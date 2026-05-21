import queue
import threading
import time
from flask import Blueprint, request, jsonify
import json

webhook_bp = Blueprint('webhook', __name__)

# 1. Giả lập một Message Queue (Trong thực tế hệ thống lớn sẽ dùng Kafka)
notification_queue = queue.Queue()

# 2. Tạo một Worker Service chạy ngầm độc lập
def email_notification_worker():
    while True:
        # Lấy event ra khỏi queue (sẽ block nếu queue rỗng)
        event = notification_queue.get()
        user_id = event['user_id']
        amount = event['amount']
        
        print(f"\n[Notification Service] Chuẩn bị gửi email cho {user_id}...")
        time.sleep(2) # Giả lập độ trễ khi gọi API gửi email (SendGrid/AWS SES)
        print(f"[Notification Service] 📧 Đã gửi biên lai {amount} VND thành công cho {user_id}!\n")
        
        notification_queue.task_done()

# Khởi chạy Worker ngầm ngay khi app start
threading.Thread(target=email_notification_worker, daemon=True).start()

# 3. Endpoint Webhook chỉ làm nhiệm vụ Publish Event
@webhook_bp.route('/webhooks/payment', methods=['POST'])
def handle_payment_webhook():
    # (Giả định đã qua bước kiểm tra chữ ký xác thực như bài trước)
    payload = request.json
    
    if payload.get("event") == "payment.success":
        user_id = payload["data"]["user_id"]
        amount = payload["data"]["amount"]
        
        # CHUẨN EVENT-DRIVEN: Không gửi email ở đây! Push vào Queue
        notification_queue.put({
            "user_id": user_id,
            "amount": amount
        })
        print(f"[Webhook Receiver] Đã đẩy event thanh toán của {user_id} vào Queue.")

    # Trả về 200 ngay lập tức, tốn chưa tới 10ms
    return jsonify({"status": "received"}), 200