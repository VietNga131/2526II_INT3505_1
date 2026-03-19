import os
import jwt
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# =====================================================================
# PHẦN THÊM MỚI: CẤU HÌNH VÀ CÁC HÀM HỖ TRỢ JWT (STATELESS)
# =====================================================================
JWT_SECRET = os.environ.get("JWT_SECRET", "secret123")
JWT_ALG = "HS256"
JWT_TTL_HOURS = 2

# Giả lập Database chứa thông tin tài khoản để đăng nhập
USERS = {
    "admin": {"password": "admin", "role": "librarian"}
}

def err(code: str, message: str, status: int):
    return jsonify({"error": {"code": code, "message": message}}), status

def create_access_token(sub: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "role": role,
        "iat": now,
        "exp": now + timedelta(hours=JWT_TTL_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def parse_bearer_token() -> str | None:
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

def require_jwt(required_role: str | None = None):
    token = parse_bearer_token()
    if not token:
        return None, err("NOT_AUTHENTICATED", "Authorization Bearer token required", 401)
    
    try:
        claims = decode_token(token)
    except jwt.ExpiredSignatureError:
        return None, err("TOKEN_EXPIRED", "Token expired", 401)
    except jwt.InvalidTokenError:
        return None, err("INVALID_TOKEN", "Invalid token", 401)
        
    if required_role and claims.get("role") != required_role:
        return None, err("FORBIDDEN", "Insufficient permission", 403)
        
    return claims, None

# Endpoint Đăng nhập để lấy Token
@app.post("/api/v1/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return err("VALIDATION_ERROR", "username and password are required", 400)
        
    user = USERS.get(username)
    if not user or user["password"] != password:
        return err("INVALID_CREDENTIALS", "Invalid username or password", 401)
        
    token = create_access_token(sub=username, role=user["role"])
    return jsonify({"token": token, "user": {"username": username, "role": user["role"]}}), 200

# Giả lập Database lưu trong RAM
users_db = [
    {"id": 1, "name": "Nguyễn Văn A"},
    {"id": 2, "name": "Trần Thị B"}
]

# --- Lớp Service (Tách biệt logic xử lý) ---
class UserService:
    @staticmethod
    def get_user_count():
        return len(users_db)

# --- Lớp Controller (Chỉ xử lý Request/Response) ---

# 1. Client-Server: Server chỉ trả dữ liệu JSON, không trả giao diện HTML
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({"data": users_db}), 200

# 2. Uniform Interface (HATEOAS): Trả về dữ liệu kèm theo các liên kết trạng thái
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Không tìm thấy"}), 404
        
    return jsonify({
        "data": user,
        "links": [
            {"rel": "self", "href": f"/api/users/{user_id}", "method": "GET"},
            {"rel": "update", "href": f"/api/users/{user_id}", "method": "PUT"},
            {"rel": "delete", "href": f"/api/users/{user_id}", "method": "DELETE"}
        ]
    }), 200

# 3. Stateless: ĐÃ CẬP NHẬT ĐỂ SỬ DỤNG JWT
@app.route('/api/secure-users', methods=['GET'])
def get_secure_users():
    # Sử dụng hàm require_jwt để kiểm tra token
    claims, error_response = require_jwt()
    
    # Nếu token không hợp lệ hoặc không có, trả về lỗi ngay lập tức
    if error_response:
        return error_response
    
    # Nếu token hợp lệ, lấy thông tin user từ token (không cần tra cứu DB hay Session)
    current_user = claims.get("sub")
    print(f"Log: User '{current_user}' đang truy cập dữ liệu bảo mật.")
    
    return jsonify({"data": users_db}), 200

# 4. Cacheable: Gắn Header báo cho Client biết có thể cache dữ liệu trong 60 giây
@app.route('/api/users/cached', methods=['GET'])
def get_users_cached():
    response = make_response(jsonify({"data": users_db}))
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response

# 5. Layered System: Controller gọi qua Service
@app.route('/api/users/count', methods=['GET'])
def count_users():
    count = UserService.get_user_count()
    return jsonify({"total_users": count}), 200

# 6. Code on Demand (Tùy chọn): Trả về script cho Client chạy
@app.route('/api/widget.js', methods=['GET'])
def get_executable_code():
    js_code = """
    console.log("Đoạn mã này được tải từ REST Server!");
    alert("Code on Demand đã hoạt động!");
    """
    return js_code, 200, {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)