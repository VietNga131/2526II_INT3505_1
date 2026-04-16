from pymongo import MongoClient
import sys

# Khởi tạo dữ liệu mồi (Mock Data)
SEED_PRODUCTS = [
    {
        "name": "Laptop Dell XPS 15",
        "price": 1800,
        "category": "Electronics"
    },
    {
        "name": "Bàn phím cơ Keychron K8",
        "price": 85,
        "category": "Accessories"
    },
    {
        "name": "Sách 'Clean Code'",
        "price": 35,
        "category": "Books"
    },
    {
        "name": "Màn hình LG UltraWide 34 inch",
        "price": 450,
        "category": "Electronics"
    },
    {
        "name": "Balo chống nước Mark Ryden",
        "price": 40,
        "category": "Fashion"
    }
]

def run_seed():
    try:
        # 1. Kết nối tới MongoDB
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["product_management_db"]
        collection = db["products"]

        print("Đang kết nối MongoDB...")
        
        # 2. Xóa dữ liệu cũ (để tránh bị trùng lặp nếu bạn chạy file này nhiều lần)
        collection.delete_many({})
        print("🗑️ Đã xóa sạch dữ liệu cũ trong collection 'products'.")

        # 3. Thêm dữ liệu mới
        result = collection.insert_many(SEED_PRODUCTS)
        
        print(f"✅ Seeding thành công! Đã thêm {len(result.inserted_ids)} sản phẩm vào Database.")
        
    except Exception as e:
        print(f"❌ Lỗi khi chạy seed data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_seed()