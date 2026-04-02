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


