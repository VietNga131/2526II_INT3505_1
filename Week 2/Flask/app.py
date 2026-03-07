from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# Giả lập Database lưu trong RAM
users_db = [
    {"id": 1, "name": "Nguyễn Văn A"},
    {"id": 2, "name": "Trần Thị B"}
]

# 1. Client-Server: Server chỉ trả dữ liệu JSON, không trả giao diện HTML
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({"data": users_db}), 200

# 2. Uniform Interface (HATEOAS): Trả về dữ liệu kèm theo các liên kết trạng thái
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Không tìm thấy"}), 404
        
    return jsonify({
        "data": user,
        "links": [
            {"rel": "self", "href": f"/api/users/{user_id}", "method": "GET"},
            {"rel": "update", "href": f"/api/users/{user_id}", "method": "PUT"},
            {"rel": "delete", "href": f"/api/users/{user_id}", "method": "DELETE"}
        ]
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)