# Demo OpenAPI & Code Generation

## 1. Mục đích
Thư mục này demo việc định nghĩa tài liệu API bằng chuẩn **OpenAPI 3.0** (Swagger) cho ứng dụng Quản lý thư viện. Sau đó, sử dụng phương pháp API-First để tự động sinh mã nguồn server (Code Generation) từ file tài liệu tĩnh.

## 2. Cấu trúc file
- `openapi.yaml`: File tài liệu gốc định nghĩa các API endpoint (`/books`).
- `generated-python-server/`: Thư mục chứa toàn bộ mã nguồn server Python (Flask) được sinh ra hoàn toàn tự động từ file yaml.

## 3. Cách sinh code tự động
Lệnh sau đã được sử dụng để tự động tạo ra thư mục `generated-python-server`:

\`\`\`bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./generated-python-server
\`\`\`

## 4. Hướng dẫn cài đặt và chạy Server, chạy Test
**Yêu cầu:** Máy tính đã cài đặt Python 3.

**Bước 1:** Di chuyển vào thư mục server đã được sinh ra
\`\`\`bash
cd generated-python-server
\`\`\`

**Bước 2:** Cài đặt các thư viện cần thiết
\`\`\`bash
py -m pip install -r requirements.txt
\`\`\`

**Bước 3:** Khởi chạy server
\`\`\`bash
py -m openapi_server
\`\`\`

**Bước 4:** Xem giao diện API
Khi terminal báo server đang chạy, hãy mở trình duyệt và truy cập vào đường dẫn sau để xem giao diện Swagger UI và test thử API:
 **http://localhost:8080/ui/**

**Bước 5:** Hướng dẫn chạy Test tự động (Automated Testing)
Quá trình Code Generation ở trên không chỉ sinh ra mã nguồn Server mà còn tự động sinh ra các kịch bản test (sử dụng `pytest`) tại thư mục `openapi_server/test/`.

**Cách chạy test:**
1. Cài đặt thư viện test:
   \`\`\`bash
   py -m pip install -r test-requirements.txt
   \`\`\`
2. Khởi chạy toàn bộ test case:
   \`\`\`bash
   py -m pytest
   \`\`\`