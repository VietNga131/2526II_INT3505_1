from flask import Flask, request, jsonify, Blueprint

app = Flask(__name__)

users_v1 = [{"id": 1, "name": "Nguyen Van A"}]
users_v2 = [{"id": 1, "first_name": "Nguyen", "last_name": "Van A", "age": 30}]

bp_v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
bp_v2 = Blueprint('v2', __name__, url_prefix='/api/v2')

# URL VERSIONING
@bp_v1.route('/users', methods=['GET'])
def get_users_v1():
    return jsonify({"version": "v1", "data": users_v1})

@bp_v2.route('/users', methods=['GET'])
def get_users_v2():
    return jsonify({"version": "v2", "data": users_v2})

# HEADER VERSIONING
@app.route('/api/users-header', methods=['GET'])
def users_header():
    version = request.headers.get('X-API-Version', '1.0')
    if version == '2.0':
        return jsonify({"version": "v2", "data": users_v2})
    return jsonify({"version": "v1", "data": users_v1})

# QUERY PARAM VERSIONING
@app.route('/api/users-query', methods=['GET'])
def users_query():
    version = request.args.get('version', '1')
    if version == '2':
        return jsonify({"version": "v2", "data": users_v2})
    return jsonify({"version": "v1", "data": users_v1})

# Đăng ký Blueprints vào app
app.register_blueprint(bp_v1)
app.register_blueprint(bp_v2)

if __name__ == '__main__':
    app.run(debug=True, port=5000)