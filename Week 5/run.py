from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Lệnh này sẽ quét qua models.py và tạo bảng nếu chưa tồn tại
        db.create_all() 
        print("✅ Đã khởi tạo các bảng trong Database!")
        
    app.run(debug=True)