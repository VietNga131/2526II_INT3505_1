import os
import uuid
from datetime import datetime, timedelta
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response, redirect

# Nạp biến môi trường
load_dotenv()

app = Flask(__name__)

# --- CẤU HÌNH ---
JWT_SECRET = os.getenv('JWT_SECRET')
REFRESH_SECRET = os.getenv('REFRESH_SECRET')
PORT = int(os.getenv('PORT', 5000))

# --- MOCK DATABASE ---
valid_refresh_tokens = set()  # Lưu Refresh Token còn hiệu lực
used_jtis = set()             # Lưu JTI đã dùng để chống Replay Attack

# ============================================================================
# UTILS: HÀM TẠO TOKEN
# ============================================================================

def create_access_token(payload):
    payload_copy = payload.copy()
    payload_copy['exp'] = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode(payload_copy, JWT_SECRET, algorithm='HS256')

def create_refresh_token(user_id):
    payload = {
        'userId': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm='HS256')

# ============================================================================
# PHẦN 1: AUTHENTICATION (LOGIN & REFRESH)
# ============================================================================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username != 'admin' or password != '123456':
        return jsonify({"message": "Sai tài khoản hoặc mật khẩu"}), 401

    payload = {
        "userId": 1,
        "username": "admin",
        "role": "admin",
        "scopes": ["read:post", "write:post"]
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(1)
    
    valid_refresh_tokens.add(refresh_token)

    # Khắc phục Token Leakage qua HttpOnly Cookie
    response = make_response(jsonify({
        "message": "Đăng nhập thành công",
        "refreshToken": refresh_token
    }))
    
    response.set_cookie(
        'access_token', 
        access_token, 
        httponly=True, 
        secure=False, # Đặt thành True nếu dùng HTTPS
        samesite='Strict',
        max_age=15 * 60
    )
    
    return response

@app.route('/api/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refreshToken')

    if not refresh_token or refresh_token not in valid_refresh_tokens:
        return jsonify({"message": "Refresh Token không hợp lệ"}), 403

    try:
        decoded = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=['HS256'])
        # Cấp access token mới
        new_payload = {"userId": decoded['userId'], "role": "admin", "scopes": ["read:post", "write:post"]}
        new_access_token = create_access_token(new_payload)

        response = make_response(jsonify({"message": "Đã cấp lại Access Token"}))
        response.set_cookie('access_token', new_access_token, httponly=True, samesite='Strict', max_age=15 * 60)
        return response
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh Token đã hết hạn"}), 403

# ============================================================================
# PHẦN 2: MIDDLEWARES (DECORATORS TRONG PYTHON)
# ============================================================================

def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        
        # Fallback sang Header
        if not token:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Truy cập bị từ chối!"}), 401

        try:
            decoded_user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user = decoded_user # Gán user vào request object của Flask
        except:
            return jsonify({"message": "Token không hợp lệ hoặc đã hết hạn!"}), 403
            
        return f(*args, **kwargs)
    return decorated

def check_permission(required_role, required_scope=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(request, 'user', None)
            role = user.get('role')
            scopes = user.get('scopes', [])

            if role != required_role and role != 'admin':
                return jsonify({"message": f"Cần role: {required_role}"}), 403

            if required_scope and (required_scope not in scopes):
                return jsonify({"message": f"Thiếu scope: {required_scope}"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================================================
# PHẦN 3: API & SECURITY AUDIT
# ============================================================================

@app.route('/api/profile')
@verify_token
def get_profile():
    return jsonify({"userInfo": request.user})

@app.route('/api/posts', methods=['POST'])
@verify_token
@check_permission('editor', 'write:post')
def create_post():
    return jsonify({"message": "Đã lưu bài viết thành công!"})

# Chống Replay Attack
@app.route('/api/generate-transaction-token', methods=['POST'])
@verify_token
def gen_trans_token():
    jti = str(uuid.uuid4())
    payload = {
        "userId": request.user['userId'],
        "action": "transfer_money",
        "jti": jti,
        "exp": datetime.utcnow() + timedelta(minutes=3)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return jsonify({"transactionToken": token})

@app.route('/api/transfer-money', methods=['POST'])
def transfer_money():
    token = request.get_json().get('transactionToken')
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        jti = decoded.get('jti')

        if jti in used_jtis:
            return jsonify({"message": "[CẢNH BÁO REPLAY ATTACK]: Token đã dùng!"}), 400

        used_jtis.add(jti)
        return jsonify({"message": "Chuyển tiền thành công!", "burned_jti": jti})
    except:
        return jsonify({"message": "Token giao dịch không hợp lệ"}), 403

# ============================================================================
# PHẦN 4: OAUTH 2.0 REDIRECT
# ============================================================================

@app.route('/auth/google')
def google_auth():
    google_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": "YOUR_GOOGLE_CLIENT_ID",
        "redirect_uri": "http://localhost:5000/auth/google/callback",
        "response_type": "code",
        "scope": "profile email"
    }

    from urllib.parse import urlencode
    return redirect(f"{google_url}?{urlencode(params)}")

if __name__ == '__main__':
    app.run(port=PORT, debug=True)