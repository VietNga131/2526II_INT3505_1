# filename=app/models.py
from . import db
from datetime import datetime

class Reader(db.Model):
    __tablename__ = 'readers'
    # Các trường dựa trên image_0.png
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    membership_date = db.Column(db.Date, default=datetime.utcnow)
    
    # Quan hệ 1-N: Một độc giả có nhiều phiếu mượn (image_2.png)
    borrows = db.relationship('BorrowRecord', backref='reader', lazy=True)

class Book(db.Model):
    __tablename__ = 'books'
    # Các trường dựa trên image_0.png
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    total_copies = db.Column(db.Integer, default=0)
    available_copies = db.Column(db.Integer, default=0)
    
    borrows = db.relationship('BorrowRecord', backref='book', lazy=True)

class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    # Các trường dựa trên image_1.png
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('readers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    # Sử dụng Enum cho status theo đúng thiết kế
    status = db.Column(db.Enum('borrowed', 'returned', 'overdue'), default='borrowed')