import requests

BASE_URL = "http://127.0.0.1:5000"

def test_client_server():
    print("--- Đóng vai trò là Client ---")
    print("1. Đang gửi Request lấy dữ liệu từ Server...\n")

    # Client chỉ yêu cầu dữ liệu, không yêu cầu giao diện
    response = requests.get(f"{BASE_URL}/api/users")

    if response.status_code == 200:
        # Nhận dữ liệu thuần túy (JSON)
        raw_data = response.json()
        print("2. Dữ liệu thuần (JSON) Server trả về:")
        print(raw_data)
        print("-" * 30)
        
        # Client tự quyết định logic hiển thị (UI) dựa trên dữ liệu đó
        print("3. Client tự render 'giao diện' cho người dùng:")
        users_list = raw_data.get('data', [])
        for user in users_list:
            print(f" 👤 ID: {user['id']} | Họ và tên: {user['name']}")
    else:
        print(f"Lỗi! Mã trạng thái: {response.status_code}")

if __name__ == "__main__":
    try:
        test_client_server()
    except requests.exceptions.ConnectionError:
        print("LỖI: Client không tìm thấy Server. Hãy đảm bảo file Flask đang chạy!")