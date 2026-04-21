import connexion
from bson.objectid import ObjectId
from bson.errors import InvalidId
from openapi_server.db import db

# Collection mục tiêu
products_collection = db["products"]

def format_product(mongo_doc):
    """
    Hàm tiện ích (Helper): 
    Chuyển đổi `_id` (ObjectId) của MongoDB thành `id` (string) để khớp với OpenAPI Spec.
    """
    if not mongo_doc:
        return None
    mongo_doc["id"] = str(mongo_doc.pop("_id"))
    return mongo_doc


def products_get():
    """Lấy danh sách toàn bộ sản phẩm"""
    try:
        # Lấy tất cả document từ collection
        cursor = products_collection.find()
        # Biến đổi _id thành id cho từng document
        product_list = [format_product(doc) for doc in cursor]
        
        return {
            "success": True,
            "message": "Lấy danh sách thành công",
            "data": product_list
        }, 200
    except Exception as e:
        return {"success": False, "message": "Lỗi Server", "error": str(e)}, 500


def products_post(body=None):
    """Thêm sản phẩm mới"""
    if connexion.request.is_json:
        body = connexion.request.get_json()
        
        new_product = {
            "name": body.get("name"),
            "price": body.get("price"),
            "category": body.get("category", "Uncategorized")
        }
        
        # Insert vào MongoDB
        result = products_collection.insert_one(new_product)
        
        # Gắn ID vừa tạo vào object để trả về cho Client
        new_product["_id"] = result.inserted_id
        
        return {
            "success": True,
            "message": "Đã tạo sản phẩm thành công",
            "data": format_product(new_product)
        }, 201
        
    return {"success": False, "message": "Dữ liệu không hợp lệ"}, 400


def products_id_get(id_):
    """Lấy chi tiết sản phẩm"""
    try:
        doc = products_collection.find_one({"_id": ObjectId(id_)})
        if doc:
            return {
                "success": True,
                "message": "Thao tác thành công",
                "data": format_product(doc)
            }, 200
            
        return {"success": False, "message": "Không tìm thấy sản phẩm", "error": "Not Found"}, 404
        
    except InvalidId: # Bắt lỗi nếu ID truyền vào không đúng format 24 hex của MongoDB
        return {"success": False, "message": "ID không đúng định dạng", "error": "Invalid ObjectId"}, 400


def products_id_put(id_, body=None):
    """Cập nhật sản phẩm"""
    if connexion.request.is_json:
        body = connexion.request.get_json()
        
        try:
            # Tạo dictionary chứa dữ liệu cần update
            update_data = {}
            if "name" in body: update_data["name"] = body["name"]
            if "price" in body: update_data["price"] = body["price"]
            if "category" in body: update_data["category"] = body["category"]

            # Thực thi update
            result = products_collection.update_one(
                {"_id": ObjectId(id_)},
                {"$set": update_data}
            )

            if result.matched_count > 0:
                # Lấy lại doc sau khi update để trả về
                updated_doc = products_collection.find_one({"_id": ObjectId(id_)})
                return {
                    "success": True,
                    "message": "Cập nhật thành công",
                    "data": format_product(updated_doc)
                }, 200
                
            return {"success": False, "message": "Không tìm thấy sản phẩm"}, 404
            
        except InvalidId:
            return {"success": False, "message": "ID không đúng định dạng"}, 400
            
    return {"success": False, "message": "Dữ liệu không hợp lệ"}, 400


def products_id_delete(id_):
    """Xóa sản phẩm"""
    try:
        result = products_collection.delete_one({"_id": ObjectId(id_)})
        
        if result.deleted_count > 0:
            return {
                "success": True,
                "message": "Xóa sản phẩm thành công",
                "data": {"id": id_}
            }, 200
            
        return {"success": False, "message": "Không tìm thấy sản phẩm", "error": "Not Found"}, 404
        
    except InvalidId:
        return {"success": False, "message": "ID không đúng định dạng"}, 400