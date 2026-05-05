from flask import Flask, request, jsonify, Blueprint

app = Flask(__name__)

# --- DỮ LIỆU GIẢ LẬP ---
users_v1 = [{"id": 1, "name": "Nguyen Van A"}]
users_v2 = [{"id": 1, "first_name": "Nguyen", "last_name": "Van A", "age": 30}] # V2 tách tên và thêm tuổi

# Cấu hình Blueprint cho từng version
bp_v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
bp_v2 = Blueprint('v2', __name__, url_prefix='/api/v2')

@bp_v1.route('/users', methods=['GET'])
def get_users_v1():
    return jsonify({"version": "v1", "data": users_v1})

@bp_v2.route('/users', methods=['GET'])
def get_users_v2():
    return jsonify({"version": "v2", "data": users_v2})

# Gắn Blueprint vào app chính
app.register_blueprint(bp_v1)
app.register_blueprint(bp_v2)

# Test: GET /api/v1/users
# Test: GET /api/v2/users