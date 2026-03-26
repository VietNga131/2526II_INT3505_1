from flask import Blueprint, request, jsonify
from .models import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/books', methods=['GET'])
def search_and_paginate_books():
    # 1. Lấy tham số từ Query String (mặc định page=1, limit=10)
    search_query = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # 2. Xây dựng Query tìm kiếm
    query = Book.query
    if search_query:
        # Tìm kiếm không phân biệt hoa thường trong tiêu đề hoặc tác giả
        query = query.filter(
            (Book.title.ilike(f"%{search_query}%")) | 
            (Book.author.ilike(f"%{search_query}%"))
        )

    # 3. Thực hiện phân trang Offset-based
    # error_out=False giúp trả về trang trống thay vì lỗi 404 nếu page vượt quá giới hạn
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    # 4. Trả về kết quả theo chuẩn Resource Design
    return jsonify({
        "data": [
            {
                "id": b.id,
                "isbn": b.isbn,
                "title": b.title,
                "author": b.author,
                "available": b.available_copies
            } for b in pagination.items
        ],
        "meta": {
            "total_records": pagination.total,
            "total_pages": pagination.pages,
            "current_page": pagination.page,
            "limit": limit,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }), 200