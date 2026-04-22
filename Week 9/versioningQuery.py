from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users_by_query():
    # Lấy giá trị của 'version' từ URL query, mặc định là '1' nếu không truyền
    version = request.args.get('version', '1')

    if version == '1':
        return jsonify({"id": 1, "name": "Alice"})
    elif version == '2':
        return jsonify({"user_id": "USR-1", "full_name": "Alice"})
    else:
        return jsonify({"error": "Version not supported"}), 400

if __name__ == '__main__':
    app.run(port=5002)