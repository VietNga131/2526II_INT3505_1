from flask import Blueprint, request, jsonify
from .models import Book, Reader, BorrowRecord
from . import db

main_bp = Blueprint('main', __name__)

# --- Helper: Chuẩn hóa định dạng phản hồi để đảm bảo tính nhất quán ---
def send_response(data=None, meta=None, message=None, code=200):
    response = {
        "status": "success" if code < 400 else "error",
        "data": data,
        "meta": meta
    }
    if message and code >= 400:
        response["message"] = message
    return jsonify(response), code

# --- ENDPOINT 1: SÁCH (Offset-based) ---
@main_bp.route('/books', methods=['GET'])
def get_books():
    """
    Tìm kiếm và phân trang sách (Offset-based)
    ---
    tags:
      - Books
    parameters:
      - name: q
        in: query
        type: string
        description: Từ khóa tìm kiếm theo tên hoặc tác giả
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
        description: Trả về danh sách sách và metadata phân trang
    """
    q = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    query = Book.query
    if q:
        query = query.filter(Book.title.ilike(f"%{q}%") | Book.author.ilike(f"%{q}%"))
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    data = [{
        "id": b.id, 
        "title": b.title, 
        "author": b.author, 
        "available": b.available_copies
    } for b in pagination.items]

    meta = {
        "total_records": pagination.total,
        "total_pages": pagination.pages,
        "current_page": page,
        "limit": limit,
        "has_next": pagination.has_next
    }
    return send_response(data=data, meta=meta)

# --- ENDPOINT 2: ĐỘC GIẢ (Offset-based) ---
@main_bp.route('/readers', methods=['GET'])
def get_readers():
    """
    Danh sách độc giả (Offset-based)
    ---
    tags:
      - Readers
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
        description: Trả về danh sách độc giả
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    pagination = Reader.query.paginate(page=page, per_page=limit, error_out=False)
    
    data = [{"id": r.id, "name": r.name, "email": r.email} for r in pagination.items]
    
    meta = {
        "total_records": pagination.total,
        "current_page": page,
        "limit": limit
    }
    return send_response(data=data, meta=meta)

# --- ENDPOINT 3: PHIẾU MƯỢN (Cursor-based) ---
@main_bp.route('/readers/<int:reader_id>/borrows', methods=['GET'])
def get_reader_borrows(reader_id):
    """
    Lịch sử mượn sách của độc giả (Cursor-based)
    ---
    tags:
      - Borrow Records
    parameters:
      - name: reader_id
        in: path
        type: integer
        required: true
      - name: after_id
        in: query
        type: integer
        default: 0
        description: ID của bản ghi cuối cùng ở trang trước
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Trả về lịch sử mượn kèm cursor để lấy trang tiếp theo
      404:
        description: Không tìm thấy độc giả
    """
    after_id = request.args.get('after_id', 0, type=int)
    limit = request.args.get('limit', 10, type=int)

    # Đảm bảo Reader tồn tại (Tính nhất quán dữ liệu)
    if not Reader.query.get(reader_id):
        return send_response(message="Reader not found", code=404)

    query = BorrowRecord.query.filter(BorrowRecord.reader_id == reader_id)
    if after_id > 0:
        query = query.filter(BorrowRecord.id > after_id)
    
    records = query.order_by(BorrowRecord.id.asc()).limit(limit).all()

    data = [{
        "id": rec.id,
        "book_title": rec.book.title,
        "borrow_date": rec.borrow_date.strftime('%Y-%m-%d'),
        "status": rec.status
    } for rec in records]

    meta = {
        "limit": limit,
        "next_cursor": data[-1]['id'] if data else None,
        "has_more": len(data) == limit
    }
    return send_response(data=data, meta=meta)