const jwt = require('jsonwebtoken');
const crypto = require('crypto');
// Giả sử bạn có thông tin user và biến môi trường
const user = { id: 123, role: 'admin' };
const JWT_SECRET = process.env.JWT_SECRET || 'your_super_secret_key';
const payload = {
    user_id: user.id,
    role:    user.role,
    // jti: JWT ID - Một mã định danh duy nhất cho token này
    jti:     crypto.randomUUID(), 
};
// jsonwebtoken tự động xử lý 'exp' nếu bạn truyền vào options
const options = {
    expiresIn: '15m',      // Tương đương timedelta(minutes=15)
    algorithm: 'HS256'
};
const token = jwt.sign(payload, JWT_SECRET, options);
console.log(token);

// Middleware kiểm tra Bearer Token
function verifyBearerToken(req, res, next) {
    // Token thường nằm ở header: "Authorization: Bearer <token>"
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ message: 'Thiếu Bearer token' });
    }

    const token = authHeader.split(' ')[1]; // Tách chữ "Bearer" ra để lấy token thật

    jwt.verify(token, 'my_secret_key', (err, decodedUser) => {
        if (err) return res.status(403).json({ message: 'Token không hợp lệ' });
        
        // Payload lúc này có thể chứa: { userId: 1, role: 'editor', scopes: ['read:post', 'write:post'] }
        req.user = decodedUser; 
        next();
    });
}


