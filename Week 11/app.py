from flask import Flask
from routes_books import books_bp
from routes_webhook import webhook_bp

app = Flask(__name__)

app.register_blueprint(books_bp, url_prefix='/api/v1')
app.register_blueprint(webhook_bp, url_prefix='/api/v1')

if __name__ == '__main__':
    print("Server is running at http://localhost:5000")
    app.run(port=5000, debug=True)