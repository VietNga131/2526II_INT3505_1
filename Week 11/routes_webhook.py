# routes_webhook.py
from flask import Blueprint, request, jsonify
import hmac
import hashlib
import json
from models import users_db

webhook_bp = Blueprint('webhook', __name__)

# Secret key được cấp bởi cổng thanh toán (chỉ bạn và cổng thanh toán biết)
WEBHOOK_SECRET = "thu_vien_secret_key_2026"

@webhook_bp.route('/webhooks/payment', methods=['POST'])
def handle_payment_webhook():
    # 1. Lấy chữ ký từ cổng thanh toán gửi sang qua Header
    signature_header = request.headers.get('X-Payment-Signature')
    payload_bytes = request.data # Lấy chuỗi byte gốc của request
    
    if not signature_header:
        return jsonify({"error": "Missing signature"}), 401

    # 2. Tạo mã băm (hash) từ payload nhận được và Secret Key của mình
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()

    # 3. So sánh chữ ký để xác thực
    if not hmac.compare_digest(expected_signature, signature_header):
        return jsonify({"error": "Invalid signature. Are you a hacker?"}), 403

    # 4. Xử lý nghiệp vụ nếu chữ ký hợp lệ
    event_data = json.loads(payload_bytes)
    
    if event_data.get("event") == "payment.success":
        user_id = event_data.get("data", {}).get("user_id")
        amount = event_data.get("data", {}).get("amount")
        
        print(f"[Webhook] Nhận thông báo thanh toán {amount} VND từ user {user_id}")
        
        # Cập nhật trạng thái người dùng trong Database
        if user_id in users_db:
            users_db[user_id]["late_fee_status"] = "PAID"
            print(f"[System] Đã xóa nợ cho user {user_id}")

    # 5. Phản hồi ngay lập tức (200 OK) để cổng thanh toán biết mình đã nhận
    # Trong hệ thống lớn, đoạn cập nhật DB ở trên nên được đẩy vào Message Queue (RabbitMQ/Kafka)
    return jsonify({"status": "Webhook received and processed"}), 200