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
    # 1. Lấy tham số từ Query String
    q = request.args.get('q', '', type=str)
    offset = request.args.get('offset', 0, type=int) # Mặc định bắt đầu từ vị trí 0
    limit = request.args.get('limit', 10, type=int)  # Mặc định lấy 10 bản ghi

    # 2. Xây dựng Query cơ bản
    query = Book.query
    if q:
        query = query.filter(Book.title.ilike(f"%{q}%") | Book.author.ilike(f"%{q}%"))
    
    # 3. Tính toán tổng số bản ghi (trước khi áp dụng offset/limit)
    total_records = query.count()
    
    # 4. Áp dụng Offset và Limit để lấy dữ liệu
    # Tương đương SQL: SELECT * FROM books WHERE ... LIMIT 10 OFFSET 0
    books = query.offset(offset).limit(limit).all()
    
    # 5. Chuyển đổi dữ liệu sang định dạng JSON
    data = [{
        "id": b.id, 
        "title": b.title, 
        "author": b.author, 
        "available": b.available_copies
    } for b in books]

    # 6. Metadata cho Offset-based
    meta = {
        "total_records": total_records,
        "offset": offset,
        "limit": limit,
        "has_more": (offset + limit) < total_records # Kiểm tra còn dữ liệu để lấy tiếp không
    }
    
    return send_response(data=data, meta=meta)

# --- ENDPOINT 2: ĐỘC GIẢ (Page-based) ---
@main_bp.route('/readers', methods=['GET'])
def get_readers():
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