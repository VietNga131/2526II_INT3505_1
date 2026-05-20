from flask import Flask
from routes_books import books_bp


app = Flask(__name__)

app.register_blueprint(books_bp, url_prefix='/api/v1')


if __name__ == '__main__':
    print("Server is running at http://localhost:5000")
    app.run(port=5000, debug=True)