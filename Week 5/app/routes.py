# filename=app/routes.py
from flask import Blueprint, request, jsonify
from .models import Book, Reader, BorrowRecord
from . import db

main_bp = Blueprint('main', __name__)

# --- ENDPOINT 1: SÁCH (Phân trang Offset-based) ---
@main_bp.route('/books', methods=['GET'])
def get_books():
    """
    Lấy danh sách sách kèm tìm kiếm và phân trang Offset
    ---
    tags: [Books]
    parameters:
      - name: q
        in: query
        type: string
        description: Từ khóa tìm kiếm (tên sách hoặc tác giả)
      - name: page
        in: query
        type: integer
        default: 1
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Thành công
    """
    search_query = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    query = Book.query
    if search_query:
        # Tìm kiếm ilike (không phân biệt hoa thường)
        query = query.filter(Book.title.ilike(f"%{search_query}%") | Book.author.ilike(f"%{search_query}%"))
    
    # Thực hiện phân trang Offset-based của SQLAlchemy
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    books = pagination.items

    return jsonify({
        "data": [
            {
                "id": b.id, "title": b.title, "author": b.author, 
                "available": b.available_copies
            } for b in books
        ],
        "meta": {
            "total_records": pagination.total,
            "total_pages": pagination.pages,
            "current_page": pagination.page,
            "has_next": pagination.has_next
        }
    }), 200

# --- ENDPOINT 2: ĐỘC GIẢ (Phân trang Offset-based) ---
@main_bp.route('/readers', methods=['GET'])
def get_readers():
    """
    Lấy danh sách độc giả kèm phân trang Offset
    ---
    tags: [Readers]
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Thành công
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    pagination = Reader.query.paginate(page=page, per_page=limit, error_out=False)
    readers = pagination.items

    return jsonify({
        "data": [{"id": r.id, "name": r.name, "email": r.email} for r in readers],
        "meta": {
            "total_records": pagination.total,
            "current_page": page
        }
    }), 200

# --- ENDPOINT 3: PHIẾU MƯỢN (Phân trang Cursor-based) ---
@main_bp.route('/readers/<int:reader_id>/borrows', methods=['GET'])
def get_reader_borrows(reader_id):
    """
    Lấy lịch sử mượn của 1 độc giả cụ thể (Phân trang Cursor)
    ---
    tags: [Borrow Records]
    parameters:
      - name: reader_id
        in: path
        type: integer
        required: true
      - name: after_id
        in: query
        type: integer
        description: ID của bản ghi cuối cùng của trang trước
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Thành công
    """
    after_id = request.args.get('after_id', 0, type=int)
    limit = request.args.get('limit', 10, type=int)

    # Đảm bảo Reader tồn tại
    Reader.query.get_or_404(reader_id)

    # Xây dựng Query Cursor-based
    # Logic: Lấy các bản ghi của Reader này, sắp xếp theo ID tăng dần, 
    # và chỉ lấy các ID lớn hơn after_id
    query = BorrowRecord.query.filter(BorrowRecord.reader_id == reader_id)
    if after_id > 0:
        query = query.filter(BorrowRecord.id > after_id)
    
    # Lấy dữ liệu (limit + 1 để kiểm tra xem còn trang sau không)
    # results = query.order_by(BorrowRecord.id.asc()).limit(limit + 1).all()
    
    # Cách làm đơn giản hơn để test: chỉ lấy đúng limit
    records = query.order_by(BorrowRecord.id.asc()).limit(limit).all()

    # Xác định cursor cho trang tiếp theo (là ID của bản ghi cuối cùng)
    next_cursor = None
    if records:
        next_cursor = records[-1].id

    return jsonify({
        "data": [
            {
                "id": rec.id,
                "book_title": rec.book.title, # Truy xuất ngược qua backref
                "borrow_date": rec.borrow_date.strftime('%Y-%m-%d'),
                "status": rec.status
            } for rec in records
        ],
        "meta": {
            "current_cursor": after_id,
            "next_cursor": next_cursor,
            "limit": limit
        }
    }), 200