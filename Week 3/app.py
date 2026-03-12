from flask import Flask, jsonify, Blueprint

app = Flask(__name__)

# =====================================================================
# 1. VERSIONING (Đánh phiên bản)
# Sử dụng Blueprint trong Flask để nhóm tất cả các API của phiên bản 1.
# Tham số url_prefix='/api/v1' đảm bảo mọi endpoint trong Blueprint này 
# đều tự động có tiền tố /api/v1 ở đầu.
# =====================================================================
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


# =====================================================================
# 2. PLURAL NOUNS & LOWERCASE (Danh từ số nhiều & Viết thường)
# Endpoint đại diện cho tập hợp tài nguyên "Sách".
# ĐÚNG: /books (Danh từ số nhiều, chữ thường)
# SAI:  /book (số ít), /GetBooks (có động từ, viết hoa)
# =====================================================================
@api_v1.route('/books', methods=['GET'])
def get_books():
    # Dữ liệu giả lập danh sách các cuốn sách
    mock_books = [
        {"id": 101, "title": "Clean Code", "author": "Robert C. Martin"},
        {"id": 102, "title": "Design Patterns", "author": "Gang of Four"}
    ]
    return jsonify(mock_books), 200


# =====================================================================
# 3. HYPHENS (Dấu gạch ngang cho từ ghép)
# Endpoint đại diện cho tập hợp "Phiếu mượn sách" (Borrow Records).
# ĐÚNG: /borrow-records (Dùng dấu gạch ngang phân tách các từ)
# SAI:  /borrowRecords (CamelCase), /borrow_records (Snake_case)
# =====================================================================

# Dữ liệu giả lập (Database)
mock_records = [
    {"id": 1, "book_id": 101, "user_id": 99, "status": "borrowed"},
    {"id": 2, "book_id": 102, "user_id": 100, "status": "returned"}
]

# =====================================================================
# TÍNH NHẤT QUÁN: CHUẨN HÓA CẤU TRÚC PHẢN HỒI (RESPONSE ENVELOPE)
# Tạo các hàm tiện ích để bọc dữ liệu vào một cấu trúc JSON cố định.
# Cấu trúc chung: { "status": "...", "message": "...", "data": {...} }
# =====================================================================

def send_success(data=None, message="Success", status_code=200):
    """Định dạng chuẩn cho các phản hồi thành công"""
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), status_code

def send_error(error_message, status_code=400, error_code="BAD_REQUEST"):
    """Định dạng chuẩn cho các phản hồi lỗi"""
    return jsonify({
        "status": "error",
        "error": {
            "code": status_code,
            "name": error_code,
            "message": error_message
        }
    }), status_code


# =====================================================================
# ÁP DỤNG TÍNH NHẤT QUÁN VÀO CÁC ENDPOINT
# =====================================================================

# 1. API Lấy danh sách phiếu mượn (Thành công)
@api_v1.route('/borrow-records', methods=['GET'])
def get_borrow_records():
    # Thay vì return jsonify(mock_records), ta dùng hàm chuẩn hóa
    return send_success(data=mock_records, message="Lấy danh sách phiếu mượn thành công")

# 2. API Lấy chi tiết 1 phiếu mượn (Xử lý cả Thành công & Lỗi)
@api_v1.route('/borrow-records/<int:record_id>', methods=['GET'])
def get_borrow_record_detail(record_id):
    # Tìm kiếm phiếu mượn trong danh sách giả lập
    record = next((r for r in mock_records if r["id"] == record_id), None)
    
    if record:
        # Nếu tìm thấy -> Trả về chuẩn Success
        return send_success(data=record, message="Lấy chi tiết phiếu mượn thành công")
    else:
        # Nếu không tìm thấy -> Trả về chuẩn Error
        return send_error(
            error_message=f"Không tìm thấy phiếu mượn với ID {record_id}", 
            status_code=404, 
            error_code="RECORD_NOT_FOUND"
        )


# =====================================================================
# TÍNH NHẤT QUÁN Ở CẤP ĐỘ FRAMEWORK (GLOBAL ERROR HANDLING)
# Bắt các lỗi do Flask tự sinh ra (như gõ sai URL) để ép về chuẩn JSON
# =====================================================================
@app.errorhandler(404)
def resource_not_found(e):
    return send_error("Đường dẫn hoặc tài nguyên không tồn tại hệ thống", 404, "ROUTE_NOT_FOUND")

@app.errorhandler(500)
def internal_server_error(e):
    return send_error("Đã xảy ra lỗi máy chủ nội bộ", 500, "INTERNAL_SERVER_ERROR")

# Đăng ký tập hợp các API v1 vào ứng dụng Flask chính
app.register_blueprint(api_v1)

if __name__ == '__main__':
    # Chạy server tại http://localhost:5000
    app.run(debug=True, port=5000)