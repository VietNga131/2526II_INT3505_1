from app import create_app, db
from flask import jsonify

app = create_app()

@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "error": "Endpoint not found", "code": 404}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "error": "Internal server error", "code": 500}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)