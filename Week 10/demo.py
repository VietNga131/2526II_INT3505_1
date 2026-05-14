import logging, requests
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from circuitbreaker import circuit, CircuitBreakerError

app = Flask(__name__)

# --- PHẦN 2: OBSERVABILITY (LOGS & METRICS) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SOA_API")
metrics = PrometheusMetrics(app) # Tự động mở endpoint /metrics

# --- PHẦN 3: SECURITY (RATE LIMITING) ---
limiter = Limiter(get_remote_address, app=app, default_limits=["100/day"])

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded", detail=str(e.description)), 429

# --- PHẦN 4: FAULT TOLERANCE (CIRCUIT BREAKER) ---
@circuit(failure_threshold=3, recovery_timeout=20)
def call_external_api():
    # Giả lập gọi service lỗi để test ngắt mạch
    resp = requests.get('http://0.0.0.0:9999', timeout=1) 
    resp.raise_for_status()
    return resp.json()

# --- ENDPOINTS DEMO ---
@app.route('/')
def home():
    logger.info("Health check accessed")
    return jsonify(status="Production Ready")

@app.route('/login', methods=['POST'])
@limiter.limit("3 per minute") # Test Rate Limit: Gửi request 4 lần/phút
def login():
    return jsonify(message="Login success")

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = call_external_api()
        return jsonify(data=data)
    except CircuitBreakerError:
        return jsonify(status="Service Degraded", message="Cầu dao đã ngắt (Fail-fast)"), 503
    except Exception:
        return jsonify(error="External service failed"), 500

if __name__ == '__main__':
    app.run()