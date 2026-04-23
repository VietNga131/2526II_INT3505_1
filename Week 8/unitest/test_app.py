import app_module

# 1. HAPPY PATH

def test_happy_path_valid_full_payload():
    """Test trường hợp gửi đầy đủ và đúng tất cả các field"""
    payload = {
        "name": "Laptop Dell",
        "description": "Laptop cho lập trình viên",
        "price": 25000000,
        "in_stock": True,
    }
    result = app_module.validate_product_payload(payload)
    assert result is None  # Kì vọng: Không có lỗi (None)

def test_happy_path_valid_partial_payload():
    """Test trường hợp update 1 phần (partial=True), ví dụ chỉ cập nhật giá"""
    payload = {
        "price": 24000000
    }
    result = app_module.validate_product_payload(payload, partial=True)
    assert result is None

# 2. EDGE CASE

def test_edge_case_empty_name_string():
    """Test trường hợp name là chuỗi rỗng"""
    payload = {"name": "", "price": 100}
    result = app_module.validate_product_payload(payload)
    assert result == 'name must be a non-empty string'

def test_edge_case_whitespace_name_string():
    """Test trường hợp name chỉ chứa khoảng trắng (người dùng cố tình lách luật)"""
    payload = {"name": "   ", "price": 100}
    result = app_module.validate_product_payload(payload)
    assert result == 'name must be a non-empty string'

def test_edge_case_price_is_zero():
    """Test trường hợp giá bằng 0 (hợp lệ về kiểu dữ liệu nhưng là số đặc biệt)"""
    payload = {"name": "Hàng tặng", "price": 0}
    result = app_module.validate_product_payload(payload)
    assert result is None

# 3. ERROR CASE

def test_error_case_payload_is_not_dict():
    """Test trường hợp payload gửi lên là 1 list hoặc string thay vì JSON object"""
    payload = ["name", "Laptop", "price", 100]
    result = app_module.validate_product_payload(payload)
    assert result == 'JSON body must be an object'

def test_error_case_missing_required_field():
    """Test trường hợp thiếu trường bắt buộc (ví dụ thiếu price)"""
    payload = {"name": "Chuột máy tính"} # Không có price
    result = app_module.validate_product_payload(payload)
    assert result == 'Missing required field: price'

def test_error_case_wrong_data_type_price():
    """Test trường hợp gửi sai kiểu dữ liệu của price (gửi chữ thay vì số)"""
    payload = {"name": "Bàn phím", "price": "Hai trăm nghìn"}
    result = app_module.validate_product_payload(payload)
    assert result == 'price must be a number'

def test_error_case_wrong_data_type_in_stock():
    """Test trường hợp gửi sai kiểu dữ liệu của in_stock (gửi số thay vì boolean True/False)"""
    payload = {"name": "Màn hình", "price": 3000000, "in_stock": 1}
    result = app_module.validate_product_payload(payload)
    assert result == 'in_stock must be a boolean'