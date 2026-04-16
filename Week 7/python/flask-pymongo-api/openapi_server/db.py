from pymongo import MongoClient
import sys

try:
    # Kết nối đến MongoDB local (hoặc thay bằng URI MongoDB Atlas)
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    
    # Kiểm tra kết nối
    client.server_info() 
    
    # Chọn database (sẽ tự động tạo nếu chưa có)
    db = client["product_management_db"]
    print("✅ Đã kết nối thành công tới MongoDB")
    
except Exception as e:
    print("❌ Lỗi kết nối MongoDB:", e)
    sys.exit(1)