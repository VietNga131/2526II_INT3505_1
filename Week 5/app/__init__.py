from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo đối tượng DB nhưng chưa gắn với app ngay (Tránh vòng lặp import)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cấu hình MySQL: mysql+pymysql://user:password@localhost/db_name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/library_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Đăng ký các Route từ file routes.py
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app