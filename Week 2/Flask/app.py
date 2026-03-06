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

if __name__ == '__main__':
    app.run(debug=True, port=5000)