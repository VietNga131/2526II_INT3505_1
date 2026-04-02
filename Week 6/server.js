require('dotenv').config(); // Nạp biến môi trường từ file .env
const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const crypto = require('crypto'); // Dùng để tạo UUID cho JTI (chống Replay Attack)

const app = express();

// --- MIDDLEWARE CƠ BẢN ---
app.use(express.json()); // Đọc body dạng JSON
app.use(cookieParser()); // Đọc HttpOnly Cookie để bảo mật token

// --- CẤU HÌNH BIẾN MÔI TRƯỜNG ---
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET;
const REFRESH_SECRET = process.env.REFRESH_SECRET;;

// --- MOCK DATABASE (Giả lập lưu trữ tạm thời) ---
const validRefreshTokens = new Set(); // Lưu các Refresh Token còn hiệu lực
const usedJtis = new Set();           // Lưu các jti (JWT ID) đã sử dụng để chống Replay Attack

// ============================================================================
// PHẦN 1: AUTHENTICATION (CẤP PHÁT TOKEN - JWT & REFRESH TOKEN)
// ============================================================================

// 1.1 ĐĂNG NHẬP: Trả về Access Token (bảo mật qua Cookie) & Refresh Token
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;

    // Kiểm tra DB giả lập (Bỏ qua hash password cho code ngắn gọn)
    if (username !== 'admin' || password !== '123456') {
        return res.status(401).json({ message: 'Sai tài khoản hoặc mật khẩu' });
    }

    // Payload: Chứa thông tin User, Role và Scopes
    const payload = { 
        userId: 1, 
        username: 'admin', 
        role: 'admin', 
        scopes: ['read:post', 'write:post'] 
    };

    // Tạo Access Token (Tuổi thọ ngắn: 15 phút)
    const accessToken = jwt.sign(payload, JWT_SECRET, { expiresIn: '15m' });

    // Tạo Refresh Token (Tuổi thọ dài: 7 ngày)
    const refreshToken = jwt.sign({ userId: 1 }, REFRESH_SECRET, { expiresIn: '7d' });
    validRefreshTokens.add(refreshToken);

    // [SECURITY AUDIT] Khắc phục Token Leakage: 
    // Thay vì gửi thẳng Access Token cho Frontend tự lưu, ta nhét vào HttpOnly Cookie
    res.cookie('access_token', accessToken, {
        httpOnly: true,     // Trình duyệt tự giữ, JavaScript không đọc được -> Chống XSS
        secure: false,      // Trong thực tế bật true (chỉ chạy trên HTTPS)
        sameSite: 'strict', // Chống CSRF Attack
        maxAge: 15 * 60 * 1000 // 15 phút
    });

    // Trả về Refresh Token (Client có thể lưu biến cục bộ hoặc bộ nhớ an toàn)
    res.json({ 
        message: 'Đăng nhập thành công, Access Token đã được set vào Cookie', 
        refreshToken: refreshToken 
    });
});

// 1.2 REFRESH TOKEN: Cấp lại Access Token mới khi token cũ hết hạn
app.post('/api/refresh', (req, res) => {
    const { refreshToken } = req.body;

    if (!refreshToken || !validRefreshTokens.has(refreshToken)) {
        return res.status(403).json({ message: 'Refresh Token không hợp lệ hoặc đã bị thu hồi' });
    }

    // Xác thực Refresh Token
    jwt.verify(refreshToken, REFRESH_SECRET, (err, decoded) => {
        if (err) return res.status(403).json({ message: 'Refresh Token đã hết hạn, vui lòng login lại' });

        // Cấp Access Token MỚI
        const payload = { userId: decoded.userId, role: 'admin', scopes: ['read:post', 'write:post'] };
        const newAccessToken = jwt.sign(payload, JWT_SECRET, { expiresIn: '15m' });

        // Ghi đè Access Token mới vào Cookie
        res.cookie('access_token', newAccessToken, {
            httpOnly: true, secure: false, sameSite: 'strict', maxAge: 15 * 60 * 1000
        });

        res.json({ message: 'Đã cấp lại Access Token thành công' });
    });
});

// ============================================================================
// PHẦN 2: MIDDLEWARES (XÁC THỰC - KIỂM TRA QUYỀN - BEARER TOKEN)
// ============================================================================

// 2.1 Middleware Xác thực (Verify Token)
function verifyToken(req, res, next) {
    // Kịch bản này hỗ trợ đọc token từ HttpOnly Cookie HOẶC từ Header chuẩn
    let token = req.cookies.access_token; // Thử đọc từ Cookie trước

    if (!token) {
        // Nếu không có Cookie, thử đọc từ "Authorization: Bearer <token>"
        const authHeader = req.headers.authorization;
        if (authHeader && authHeader.startsWith('Bearer ')) {
            token = authHeader.split(' ')[1];
        }
    }

    if (!token) return res.status(401).json({ message: 'Truy cập bị từ chối. Không tìm thấy Token!' });

    // Xác thực Token
    jwt.verify(token, JWT_SECRET, (err, decodedUser) => {
        if (err) return res.status(403).json({ message: 'Token không hợp lệ hoặc đã hết hạn!' });
        
        req.user = decodedUser; // Gắn dữ liệu giải mã được vào req để API phía sau dùng
        next(); // Chuyển quyền xử lý sang API
    });
}

// 2.2 Middleware Phân quyền (Role & Scope)
function checkPermission(requiredRole, requiredScope) {
    return (req, res, next) => {
        const { role, scopes } = req.user;

        // 1. Kiểm tra Role
        if (role !== requiredRole && role !== 'admin') {
            return res.status(403).json({ message: `Từ chối truy cập. Cần role: ${requiredRole}` });
        }

        // 2. Kiểm tra Scope (Nghiệp vụ sâu hơn)
        if (requiredScope && (!scopes || !scopes.includes(requiredScope))) {
            return res.status(403).json({ message: `Từ chối truy cập. Token thiếu scope: ${requiredScope}` });
        }

        next();
    };
}

// ============================================================================
// PHẦN 3: BẢO VỆ API & SECURITY AUDIT (CHỐNG REPLAY ATTACK)
// ============================================================================

// 3.1 API lấy Profile: Ai có token hợp lệ đều gọi được
app.get('/api/profile', verifyToken, (req, res) => {
    res.json({ message: 'Xin chào!', userInfo: req.user });
});

// 3.2 API đăng bài: Bắt buộc phải là Editor và có scope 'write:post'
app.post('/api/posts', verifyToken, checkPermission('editor', 'write:post'), (req, res) => {
    res.json({ message: 'Đã lưu bài viết thành công lên DB!' });
});

// 3.3 [SECURITY AUDIT] - Chống Replay Attack (Tấn công phát lại)
// BƯỚC A: Cấp 1 token giao dịch chỉ dùng 1 lần (Single-use token)
app.post('/api/generate-transaction-token', verifyToken, (req, res) => {
    const payload = { 
        userId: req.user.userId, 
        action: 'transfer_money',
        jti: crypto.randomUUID() // JTI (JWT ID) - Chuỗi định danh duy nhất cho token này
    };
    // Token này chỉ sống 3 phút, ép người dùng thao tác nhanh
    const transactionToken = jwt.sign(payload, JWT_SECRET, { expiresIn: '3m' }); 
    res.json({ transactionToken });
});

// BƯỚC B: Thực hiện giao dịch và đốt (burn) cái jti đó đi
app.post('/api/transfer-money', (req, res) => {
    const { transactionToken } = req.body;
    if (!transactionToken) return res.status(400).json({ message: 'Thiếu Transaction Token' });

    jwt.verify(transactionToken, JWT_SECRET, (err, decoded) => {
        if (err) return res.status(403).json({ message: 'Token giao dịch không hợp lệ' });

        const { jti, action } = decoded;

        // KIỂM TRA LỖ HỔNG REPLAY ATTACK
        // Có ai đó đang copy nguyên cái request cũ gửi lại để rút tiền lần 2 không?
        if (usedJtis.has(jti)) {
            return res.status(400).json({ 
                message: '[CẢNH BÁO REPLAY ATTACK]: Token này đã được sử dụng. Giao dịch bị từ chối!' 
            });
        }

        if (action !== 'transfer_money') {
            return res.status(403).json({ message: 'Token không dành cho chức năng này' });
        }

        // Logic trừ tiền thành công...
        
        // Đánh dấu jti này là "đồ bỏ đi" (Thực tế sẽ lưu vào Redis)
        usedJtis.add(jti);

        res.json({ message: 'Chuyển tiền thành công!', jti_burned: jti });
    });
});

// ============================================================================
// PHẦN 4: OAUTH 2.0 (MINH HỌA FLOW ỦY QUYỀN)
// ============================================================================

// API Redirect user sang Server của Google
app.get('/auth/google', (req, res) => {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    
    // Các tham số bắt buộc của OAuth 2.0
    const params = new URLSearchParams({
        client_id: 'YOUR_GOOGLE_CLIENT_ID', // Client ID lấy từ Google Cloud Console
        redirect_uri: 'http://localhost:3000/auth/google/callback', // Đường dẫn hứng code Google trả về
        response_type: 'code',
        scope: 'profile email', // Xin quyền đọc Profile và Email
    });
    
    // Bật trình duyệt sang trang đăng nhập của Google
    res.redirect(`${googleAuthUrl}?${params.toString()}`);
});

// ============================================================================
// KHỞI ĐỘNG SERVER
// ============================================================================
app.listen(PORT, () => {
    console.log(`🚀 Server đang chạy tại: http://localhost:${PORT}`);
    console.log(`\n--- HƯỚNG DẪN TEST NHANH BẰNG POSTMAN ---`);
    console.log(`1. Gửi POST đến http://localhost:${PORT}/api/login`);
    console.log(`   Body (JSON): { "username": "admin", "password": "123456" }`);
    console.log(`2. Test API bảo mật: Gửi GET đến http://localhost:${PORT}/api/profile`);
    console.log(`   (Không cần gắn token thủ công vì nó đã tự lưu vào Cookie)`);
});