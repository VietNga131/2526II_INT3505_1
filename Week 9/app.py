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


# CASE STUDY: PAYMENT

# TẦNG SERVICE (Business Logic cốt lõi)

class PaymentService:
    @staticmethod
    def execute_payment(value, currency, method):
        # Giả lập xử lý thành công
        return {
            "processed_value": value,
            "currency": currency,
            "method": method
        }



# TẦNG CONTROLLER (Routes / Xử lý I/O)

# --- V1: Legacy Endpoint (Adapter) ---
@bp_v1.route('/payments', methods=['POST'])
def process_payment_v1():
    # Nhận I/O từ Request
    data = request.json or {}
    amount = data.get('amount')
    
    # Adapter: Gọi Service với các thông số mặc định cho app cũ
    PaymentService.execute_payment(
        value=amount, 
        currency="VND",
        method="UNKNOWN_CARD"
    )
    
    # Format Response trả về
    response = jsonify({
        "status": "success",
        "message": "Payment processed (v1)",
        "processed_amount": amount,
        "warning": "This endpoint is deprecated. Upgrade to v2."
    })
    
    # Gắn Header cảnh báo Deprecation
    response.headers['Deprecation'] = 'true'
    response.headers['Warning'] = '299 - "This API version is deprecated and will be removed on 2026-12-31."'
    
    return response, 200


# --- V2: Modern Endpoint ---
@bp_v2.route('/payments', methods=['POST'])
def process_payment_v2():
    # Nhận và Validate I/O
    data = request.json or {}
    amount = data.get('amount')
    payment_method = data.get('paymentMethod')

    # Validate bắt buộc theo chuẩn mới
    if not amount or 'currency' not in amount or not payment_method:
        return jsonify({"error": "Missing new required fields (currency, paymentMethod)"}), 400
    
    # Gọi Service xử lý cốt lõi bằng dữ liệu chuẩn mới
    service_result = PaymentService.execute_payment(
        value=amount.get('value'),
        currency=amount.get('currency'),
        method=payment_method
    )
    
    # Format Response trả về
    return jsonify({
        "status": "success",
        "message": "Payment processed successfully (v2)",
        "details": f"{service_result['processed_value']} {service_result['currency']} via {service_result['method']}"
    }), 200

# Đăng ký Blueprints vào app
app.register_blueprint(bp_v1)
app.register_blueprint(bp_v2)

if __name__ == '__main__':
    app.run(debug=True, port=5000)