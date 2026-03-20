# Demo RAML: Library Management System

## 1. Mục đích
Thư mục này demo việc thiết kế API bằng **RAML 1.0**. Chuẩn RAML có thế mạnh lớn trong việc tổ chức file gọn gàng và hệ sinh thái hỗ trợ sinh giao diện tài liệu (HTML) rất chuyên nghiệp.

## 2. File cấu hình
- `api.raml`: File gốc định nghĩa cấu trúc API và các kiểu dữ liệu (Types).
- `index.html`: File tài liệu tĩnh được sinh ra tự động từ `api.raml`.

## 3. Hướng dẫn sinh tài liệu HTML (Doc Generation)
Công cụ `raml2html` được sử dụng để dịch file RAML thành giao diện web trực quan.
\`\`\`bash
npx raml2html api.raml > index.html
\`\`\`
*(Mở file `index.html` bằng trình duyệt để xem kết quả).*

## 4. Hướng dẫn chạy Mock Server để Test API
Dùng công cụ `osprey-mock-service` để đọc file RAML và tự động tạo server giả lập, giúp Frontend có thể test gọi API ngay lập tức mà không cần code Backend.
\`\`\`bash
npx osprey-mock-service -f api.raml -p 3000
\`\`\`
*(Server sẽ chạy tại `http://localhost:3000`. Thử truy cập `http://localhost:3000/books` để xem dữ liệu trả về).*