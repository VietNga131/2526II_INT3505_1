# Demo TypeSpec: Compile & Test Generation

## 1. Mục đích
Thư mục này demo **TypeSpec** (Microsoft). Khác với các chuẩn khác, lập trình viên sẽ viết code TypeSpec (giống TypeScript), sau đó biên dịch (Compile) ra chuẩn OpenAPI 3.0. Từ file OpenAPI này, ta có thể dùng hệ sinh thái tool đồ sộ để sinh Server hoặc sinh Mock Server để test.

## 2. File cấu hình
- `main.tsp`: File mã nguồn gốc viết bằng TypeSpec.

## 3. Cài đặt môi trường
\`\`\`bash
npm init -y
npm install @typespec/compiler @typespec/http @typespec/openapi3
\`\`\`

## 4. Demo Sinh Code (Compile TypeSpec -> OpenAPI)
Chạy lệnh sau để bộ biên dịch đọc file `main.tsp` và đẻ ra file `openapi.yaml`:
\`\`\`bash
npx tsp compile main.tsp --emit @typespec/openapi3
\`\`\`
*(Thành quả: File `openapi.yaml` được tạo ra trong thư mục `tsp-output/@typespec/openapi3/`)*

## 5. Demo Test (Sinh Mock Server từ file vừa compile)
Sử dụng công cụ **Prism** để đọc file OpenAPI vừa sinh ra và tự động dựng Server giả lập, giúp kiểm thử API ngay lập tức:
\`\`\`bash
npx @stoplight/prism-cli mock tsp-output/@typespec/openapi3/openapi.yaml
\`\`\`
*(Server test sẽ chạy tại `http://127.0.0.1:4010`. Mở trình duyệt và truy cập `http://127.0.0.1:4010/books` để xem kết quả trả về).*