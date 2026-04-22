from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users_by_header():
    # Đọc custom header 'X-API-Version'. Mặc định cho dùng v1.
    version = request.headers.get('X-API-Version', '1')

    if version == '1':
        return jsonify({"id": 1, "name": "Alice"})
    elif version == '2':
        return jsonify({"user_id": "USR-1", "full_name": "Alice"})
    else:
        return jsonify({"error": "Unsupported API Version. Please use 1 or 2."}), 400

if __name__ == '__main__':
    app.run(port=5003)