import jwt
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = "chuoi_khoa_bi_mat_cua_server"

@app.route('/login', methods=['POST'])
def login():
    """
    [Cơ chế hoạt động - Bước 1]: Client nhận token sau khi login
    """
    payload = {
        "user_id": 123,
        # [Rủi ro - Giải pháp]: Set thời hạn token ngắn (15 phút) 
        # Giúp giảm thiểu rủi ro bị kẻ gian "đánh cắp" và "dùng ngay để giả mạo" mãi mãi.
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    
    # Sinh ra mã token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})


@app.route('/api/profile', methods=['GET'])
def get_profile():
    """
    [Cách dùng trong HTTP Header]: Mô phỏng Endpoint GET /api/profile
    """
    # [Cơ chế hoạt động - Bước 3]: Flask đọc header
    # Tìm kiếm Header có tên là "Authorization"
    auth_header = request.headers.get('Authorization')
    
    # Kiểm tra xem Header có tồn tại và có bắt đầu bằng chữ "Bearer " hay không 
    # (Đúng quy tắc: Header Authorization với prefix Bearer)
    if auth_header and auth_header.startswith("Bearer "):
        
        # Tách chuỗi khoảng trắng để lấy đoạn mã thật sự (bỏ chữ "Bearer" đi)
        token = auth_header.split(" ")[1]
        
        try:
            # [Cơ chế hoạt động - Bước 3]: verify token
            # Hàm decode tự động kiểm tra chữ ký và đối chiếu thời gian (exp) xem đã quá 15 phút chưa
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            
            # [Cơ chế hoạt động - Bước 4]: Nếu hợp lệ → cấp quyền truy cập
            return jsonify({
                "message": "Truy cập thành công!", 
                "data": f"Thông tin profile của user ID: {decoded['user_id']}"
            }), 200
            
        except jwt.ExpiredSignatureError:
            # Chặn ngay nếu kẻ gian dùng token bị đánh cắp nhưng đã quá 15 phút
            return jsonify({"error": "Token đã hết hạn 15 phút. Vui lòng login lại!"}), 401
            
        except jwt.InvalidTokenError:
            # Chặn nếu token bị chỉnh sửa, làm giả (sai chữ ký)
            return jsonify({"error": "Token không hợp lệ hoặc bị giả mạo!"}), 401
            
    # Chặn nếu request gửi lên mà không có token (Không có vé thì không được vào)
    return jsonify({"error": "Không tìm thấy Bearer Token trong header!"}), 401

if __name__ == '__main__':
    # Lưu ý: Luôn chạy trên HTTPS ở môi trường thực tế (như ảnh cảnh báo)
    app.run()