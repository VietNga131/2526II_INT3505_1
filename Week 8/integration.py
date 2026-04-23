import requests

def test_integration_login_and_get_profile():
    base_url = "https://dummyjson.com"

    # BƯỚC 1: Gọi Auth Service (Đăng nhập)

    login_payload = {
        "username": "emilys",       # Tài khoản test có sẵn của DummyJSON
        "password": "emilyspass"
    }
    response_login = requests.post(f"{base_url}/auth/login", json=login_payload)
    
    # Đảm bảo API trả về 200 OK
    assert response_login.status_code == 200, "Lỗi: Đăng nhập thất bại!"
    
    # Trích xuất JWT (JSON Web Token)
    token = response_login.json().get("accessToken")
    assert token is not None, "Lỗi: Không nhận được Token!"

    # BƯỚC 2: Gọi Profile API với Token vừa lấy

    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Truy cập endpoint /auth/me (bắt buộc phải có token)
    response_profile = requests.get(f"{base_url}/auth/me", headers=headers)

    # BƯỚC 3: Kiểm tra sự kết hợp (Integration Assertions)

    assert response_profile.status_code == 200, "Lỗi: Lấy profile thất bại!"
    
    profile = response_profile.json()
    
    # Xác nhận API trả về đúng cấu trúc và đúng người dùng
    assert "id" in profile
    assert "email" in profile
    assert "firstName" in profile
    assert profile["username"] == "emilys"
    
    print(f"\n✅ Luồng tích hợp thành công! Đã lấy được profile của: {profile['firstName']} {profile['lastName']}")