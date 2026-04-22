from flask import Flask, jsonify

app = Flask(__name__)

# Phiên bản 1: Trả về cấu trúc đơn giản
@app.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    return jsonify({
        "version": "v1",
        "data": [{"id": 1, "name": "Alice"}]
    })

# Phiên bản 2: Trả về cấu trúc chi tiết hơn (Breaking Change)
@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    return jsonify({
        "version": "v2",
        "data": [{"user_id": "USR-1", "full_name": "Alice", "role": "admin"}]
    })

if __name__ == '__main__':
    app.run(port=5001)