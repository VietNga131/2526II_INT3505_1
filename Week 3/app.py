from flask import Flask, jsonify, request, Blueprint

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
# TÍNH DỄ HIỂU (CLARITY): SỬ DỤNG ĐÚNG HTTP METHODS CHO TỪNG NGHIỆP VỤ
# =====================================================================

# Nghiệp vụ 1: Lấy danh sách phiếu mượn (Method: GET)
@api_v1.route('/borrow-records', methods=['GET'])
def get_borrow_records():
    return send_success(data=mock_records, message="Lấy danh sách phiếu mượn thành công")

# Nghiệp vụ 2: MƯỢN SÁCH (Tạo phiếu mượn mới -> Method: POST)
# Thay vì dùng URL /create-borrow-record hoặc /muon-sach
@api_v1.route('/borrow-records', methods=['POST'])
def borrow_book():
    # Lấy dữ liệu người dùng gửi lên qua Body (JSON)
    req_data = request.get_json()
    
    # Kiểm tra tính hợp lệ của dữ liệu (Validation)
    if not req_data or 'book_id' not in req_data or 'user_id' not in req_data:
        return send_error("Thiếu thông tin book_id hoặc user_id.", 400)
    
    # Logic tạo mới (Giả lập tăng ID tự động)
    new_id = max([r['id'] for r in mock_records]) + 1 if mock_records else 1
    new_record = {
        "id": new_id,
        "book_id": req_data['book_id'],
        "user_id": req_data['user_id'],
        "status": "borrowed"
    }
    
    # Lưu vào "Database"
    mock_records.append(new_record)
    
    # Trả về mã 201 Created (Chuẩn HTTP cho việc tạo tài nguyên thành công)
    return send_success(data=new_record, message="Mượn sách thành công", status_code=201)


# Nghiệp vụ 3: TRẢ SÁCH (Cập nhật trạng thái phiếu mượn -> Method: PATCH)
# Thay vì dùng URL /return-book, ta cập nhật tài nguyên cụ thể qua ID
@api_v1.route('/borrow-records/<int:record_id>', methods=['PATCH'])
def return_book(record_id):
    req_data = request.get_json()
    
    # Ràng buộc: Chỉ chấp nhận hành động cập nhật status thành 'returned'
    if not req_data or req_data.get('status') != 'returned':
        return send_error("Dữ liệu không hợp lệ. Để trả sách, hãy gửi status là 'returned'.", 400)
    
    # Tìm phiếu mượn trong DB
    record = next((r for r in mock_records if r["id"] == record_id), None)
    
    if not record:
        return send_error(f"Không tìm thấy phiếu mượn với ID {record_id}", 404)
    
    if record['status'] == 'returned':
        return send_error("Sách này đã được trả trước đó rồi.", 400)

    # Cập nhật trạng thái
    record['status'] = 'returned'
    
    # Trả về 200 OK
    return send_success(data=record, message=f"Đã trả sách cho phiếu mượn {record_id} thành công")


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