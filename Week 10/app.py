from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
import pybreaker
import logging

app = Flask(__name__)

# 1. THIẾT LẬP LOGGING (Audit Logs & Error Logs)
# Trong production, log thường được xuất ra dạng JSON để đẩy lên ELK Stack hoặc Datadog.
# Ở đây ta dùng format text chuẩn để dễ quan sát trên terminal.
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api_service")


# 2. THIẾT LẬP MONITORING (Prometheus Metrics)
# Exporter sẽ tự động theo dõi các HTTP requests và tạo endpoint '/metrics'
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')


# 3. THIẾT LẬP RATE LIMITING (Security)
# Giới hạn số lượng request để chống Spam/DDoS.
# Lưu ý: Trong production, storage_uri nên trỏ về Redis (VD: "redis://localhost:6379")
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://" 
)

# 4. THIẾT LẬP CIRCUIT BREAKER
# Nếu gọi 1 external service lỗi 3 lần liên tiếp, Circuit Breaker sẽ "Mở" (Open).
# Mọi request tiếp theo sẽ bị chặn ngay lập tức trong 10 giây (reset_timeout) để service kia phục hồi.
db_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)


# 5. ENDPOINTS THỰC HÀNH

@app.route('/api/public-data', methods=['GET'])
@limiter.limit("5 per minute") # Custom rate limit: Tối đa 5 req/phút cho IP
def get_public_data():
    """Endpoint có Rate Limit và Audit Log"""
    # Audit log ghi lại ai đang gọi API
    logger.info(f"Endpoint /api/public-data được gọi bởi IP: {request.remote_addr}")
    
    return jsonify({
        "status": "success",
        "message": "Dữ liệu trả về thành công!",
        "data": {"id": 1, "name": "Service Operation"}
    })


# Hàm giả lập gọi External Service (có thể là Database hoặc API khác)
@db_breaker
def call_flaky_external_service():
    """Hàm này mô phỏng một service đang bị sập hoặc timeout"""
    logger.warning("Đang cố gắng kết nối tới External Service...")
    raise Exception("Connection Timeout!") # Luôn văng lỗi để test


@app.route('/api/external', methods=['GET'])
def get_external_data():
    """Endpoint có bọc Circuit Breaker"""
    try:
        call_flaky_external_service()
        return jsonify({"status": "success", "message": "Kết nối thành công"})
    
    except pybreaker.CircuitBreakerError:
        # Lỗi này văng ra khi Breaker đang ở trạng thái OPEN (Mở)
        logger.error("CIRCUIT BREAKER OPEN: Đã ngắt kết nối để bảo vệ hệ thống!")
        return jsonify({
            "status": "error", 
            "message": "Hệ thống phụ thuộc đang quá tải. Vui lòng thử lại sau 10 giây."
        }), 503
        
    except Exception as e:
        # Lỗi này văng ra ở 3 lần đầu tiên gọi service bị lỗi
        logger.error(f"Lỗi từ External Service: {str(e)}")
        return jsonify({"status": "error", "message": "Lỗi xử lý nội bộ"}), 500


if __name__ == '__main__':
    # KHÔNG DÙNG app.run() trong production. Phải dùng Gunicorn hoặc uWSGI.
    # Lệnh chạy production: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    app.run(host='0.0.0.0', port=5000, debug=False)