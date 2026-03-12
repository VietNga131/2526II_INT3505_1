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
@api_v1.route('/borrow-records', methods=['GET'])
def get_borrow_records():
    # Dữ liệu giả lập danh sách phiếu mượn
    mock_records = [
        {"id": 1, "book_id": 101, "user_id": 99, "status": "borrowed"},
        {"id": 2, "book_id": 102, "user_id": 100, "status": "returned"}
    ]
    return jsonify(mock_records), 200


# Đăng ký tập hợp các API v1 vào ứng dụng Flask chính
app.register_blueprint(api_v1)

if __name__ == '__main__':
    # Chạy server tại http://localhost:5000
    app.run(debug=True, port=5000)