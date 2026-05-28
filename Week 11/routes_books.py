from flask import Blueprint, request, jsonify
from models import books_db

books_bp = Blueprint('books', __name__)

def format_book_hateoas(book):
    """Hàm helper format response theo chuẩn HATEOAS"""
    book_id = book['id']
    status = book['status']

    response = {
        "data": book,
        "_links": {
            "self": f"/api/v1/books/{book_id}"
        }
    }

    if status == "AVAILABLE":
        response["_links"]["borrow"] = {
            "href": f"/api/v1/books/{book_id}/borrow",
            "method": "POST"
        }
    elif status == "BORROWED":
        response["_links"]["return"] = {
            "href": f"/api/v1/books/{book_id}/return",
            "method": "POST"
        }

    return response

# --- CRUD & QUERY PATTERNS ---

@books_bp.route('/books', methods=['GET'])
def get_books():
    """Query Pattern: Lấy danh sách sách có hỗ trợ filter theo category và status"""
    category_filter = request.args.get('category')
    status_filter = request.args.get('status')

    results = []
    for b_id, book in books_db.items():
        if category_filter and book['category'] != category_filter:
            continue
        if status_filter and book['status'] != status_filter:
            continue

        results.append(format_book_hateoas(book))

    return jsonify({
        "total": len(results),
        "items": results
    }), 200

@books_bp.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """Read: Lấy thông tin 1 quyển sách"""
    if book_id not in books_db:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(format_book_hateoas(books_db[book_id])), 200

@books_bp.route('/books', methods=['POST'])
def create_book():
    """Create: Thêm sách mới"""
    data = request.json
    book_id = data.get('id')
    if not book_id or book_id in books_db:
        return jsonify({"error": "Invalid or duplicate book ID"}), 400
    
    new_book = {
        "id": book_id,
        "title": data.get('title', 'Unknown'),
        "category": data.get('category', 'Uncategorized'),
        "status": data.get('status', 'AVAILABLE')
    }
    books_db[book_id] = new_book
    return jsonify({"message": "Book created successfully", "book": format_book_hateoas(new_book)}), 201

@books_bp.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """Update: Cập nhật thông tin sách"""
    if book_id not in books_db:
        return jsonify({"error": "Book not found"}), 404
    
    data = request.json
    books_db[book_id].update({
        "title": data.get('title', books_db[book_id]['title']),
        "category": data.get('category', books_db[book_id]['category']),
        "status": data.get('status', books_db[book_id]['status'])
    })
    return jsonify({"message": "Book updated successfully", "book": format_book_hateoas(books_db[book_id])}), 200

@books_bp.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete: Xóa sách"""
    if book_id not in books_db:
        return jsonify({"error": "Book not found"}), 404
    del books_db[book_id]
    return jsonify({"message": "Book deleted successfully"}), 200

# --- HATEOAS STATE TRANSITIONS ---

@books_bp.route('/books/<book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    """Action: Mượn sách (Thay đổi state)"""
    if book_id not in books_db:
        return jsonify({"error": "Book not found"}), 404
    
    if books_db[book_id]["status"] != "AVAILABLE":
        return jsonify({"error": "Book is not available for borrowing"}), 400
    
    books_db[book_id]["status"] = "BORROWED"
    return jsonify({
        "message": "Book borrowed successfully", 
        "book": format_book_hateoas(books_db[book_id])
    }), 200

@books_bp.route('/books/<book_id>/return', methods=['POST'])
def return_book(book_id):
    """Action: Trả sách (Thay đổi state)"""
    if book_id not in books_db:
        return jsonify({"error": "Book not found"}), 404
    
    if books_db[book_id]["status"] != "BORROWED":
        return jsonify({"error": "Book is not currently borrowed"}), 400
    
    books_db[book_id]["status"] = "AVAILABLE"
    return jsonify({
        "message": "Book returned successfully", 
        "book": format_book_hateoas(books_db[book_id])
    }), 200