from flask import Flask, url_for, session, redirect
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') # Dùng để bảo mật session

# Cấu hình OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f"Xin chào {user['name']}! <a href='/logout'>Đăng xuất</a>"
    return '<a href="/login">Đăng nhập bằng Google</a>'

@app.route('/login')
def login():
    # Bước 1: Redirect người dùng sang Google
    redirect_uri = url_for('auth', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth')
def auth():
    # Bước 3 & 4: Nhận code và đổi lấy token
    token = google.authorize_access_token()
    
    # TINH CHỈNH TẠI ĐÂY: Trích xuất trực tiếp thông tin từ trong token
    user_info = token.get('userinfo')
    
    # Lưu thông tin user vào session
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)