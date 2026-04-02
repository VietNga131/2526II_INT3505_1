from app import create_app, db
from app.models import Book, Reader, BorrowRecord
from datetime import datetime, timedelta
import random

app = create_app()

def seed_database():
    with app.app_context():
        print("--- Đang khởi tạo lại Database ---")
        db.drop_all()   # Xóa bảng cũ để đảm bảo dữ liệu sạch
        db.create_all() # Tạo lại bảng mới từ models.py

        # 1. Nạp dữ liệu Sách (25 cuốn để test phân trang limit=10)
        book_titles = [
            "Clean Code", "Refactoring", "Design Patterns", "The Clean Architect",
            "Domain-Driven Design", "Microservices Patterns", "Python Crash Course",
            "Flask Web Development", "SQL Cookbook", "Modern Operating Systems",
            "Compilers: Principles", "Computer Networking", "Artificial Intelligence",
            "Data Science from Scratch", "Deep Learning with Python", "Fluent Python",
            "Algorithms Unlocked", "Code Complete", "The Mythical Man-Month",
            "Soft Skills", "Pragmatic Programmer", "Test Driven Development",
            "Building Microservices", "Site Reliability Engineering", "Effective Java"
        ]
        
        books = []
        for i, title in enumerate(book_titles):
            b = Book(
                id=100 + i, # ID cố định để dễ quản lý
                title=title,
                author=f"Author {i+1}",
                isbn=f"ISBN-978-{1000+i}",
                total_copies=10,
                available_copies=8
            )
            books.append(b)
            db.session.add(b)
        
        # 2. Nạp dữ liệu Độc giả (5 người)
        readers = []
        for i in range(1, 6):
            r = Reader(
                name=f"Độc giả {i}",
                email=f"reader{i}@example.com",
                phone=f"090123456{i}"
            )
            readers.append(r)
            db.session.add(r)
        
        db.session.commit() # Lưu để có ID cho bảng BorrowRecord

        # 3. Nạp dữ liệu Phiếu mượn (15 bản ghi cho Reader 1 để test Cursor)
        print("--- Đang nạp lịch sử mượn cho Độc giả 1 ---")
        reader_1 = readers[0]
        for i in range(1, 16):
            loan = BorrowRecord(
                reader_id=reader_1.id,
                book_id=random.choice(books).id,
                borrow_date=datetime.utcnow() - timedelta(days=i),
                due_date=datetime.utcnow() + timedelta(days=7),
                status=random.choice(['borrowed', 'returned', 'overdue'])
            )
            db.session.add(loan)

        db.session.commit()
        print("✅ Thành công: Đã nạp 25 sách, 5 độc giả và 15 phiếu mượn!")

if __name__ == '__main__':
    seed_database()