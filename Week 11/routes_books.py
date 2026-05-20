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

@books_bp.route('/books', methods=['GET'])
def get_books():
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

@books_bp.route('/books/<book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    if book_id not in books_db:
        return jsonify({"error": "Book not found"}), 404
    
    if books_db[book_id]["status"] != "AVAILABLE":
        return jsonify({"error": "Book is not available for borrowing"}), 400
    
    books_db[book_id]["status"] = "BORROWED"
    return jsonify({"message": "Book borrowed successfully", "book": books_db[book_id]}), 200