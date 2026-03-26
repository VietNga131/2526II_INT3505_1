from app import create_app, db
from app.models import Book, Reader
import random

app = create_app()

def seed_database():
    with app.app_context():
        # 1. Xóa dữ liệu cũ (nếu muốn làm sạch để test lại)
        # db.drop_all() 
        # db.create_all()

        # 2. Tạo dữ liệu mẫu cho Sách
        sample_books = [
            ("Clean Code", "Robert C. Martin", "9780132350884"),
            ("The Pragmatic Programmer", "Andrew Hunt", "9780201616224"),
            ("Design Patterns", "Erich Gamma", "9780201633610"),
            ("Introduction to Algorithms", "Thomas H. Cormen", "9780262033848"),
            ("Refactoring", "Martin Fowler", "9780134757599"),
            ("Head First Design Patterns", "Eric Freeman", "9780596007126"),
            ("The Mythical Man-Month", "Frederick Brooks", "9780201835953"),
            ("Code Complete", "Steve McConnell", "9780735619678"),
            ("Soft Skills", "John Sonmez", "9781617292392"),
            ("Cracking the Coding Interview", "Gayle Laakmann", "9780984782857")
        ]

        print("Đang nạp dữ liệu sách...")
        for i in range(1, 21):  # Tạo 20 cuốn sách
            title, author, isbn_base = random.choice(sample_books)
            new_book = Book(
                title=f"{title} - Tập {i}",
                author=author,
                isbn=f"{isbn_base}{i}",
                total_copies=5,
                available_copies=5
            )
            db.session.add(new_book)

        # 3. Tạo 1 Độc giả mẫu
        if not Reader.query.filter_by(email="fpt_student@uet.vnu.edu.vn").first():
            reader = Reader(
                name="FPT Student",
                email="fpt_student@uet.vnu.edu.vn",
                phone="0912345678"
            )
            db.session.add(reader)

        db.session.commit()
        print("✅ Đã nạp dữ liệu mẫu thành công!")

if __name__ == '__main__':
    seed_database()