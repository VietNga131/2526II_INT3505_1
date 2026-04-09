# Demo API Blueprint & Test Generation

## 1. Mục đích
Thư mục này demo việc thiết kế API bằng định dạng Markdown của **API Blueprint**. Thế mạnh cốt lõi của Blueprint là khả năng sinh Mock Server (Server giả lập) và sinh kịch bản Kiểm thử tự động (Automated Contract Testing) cực kỳ nhanh chóng.

## 2. File cấu hình
- `api.apib`: File tài liệu API viết bằng Blueprint (Lưu ý định dạng end-of-line phải là `LF`).

## 3. Cách chạy Demo (Gồm 2 Terminal chạy song song)
**Xem demo**
Khởi động server: drakov -f api.apib -p 3000
Xem kết quả: http://localhost:3000/books

**Bước 1: Chạy Mock Server (Terminal 1)**
Công cụ `drakov` đọc file tài liệu và tự động dựng lên một server giả lập.
\`\`\`bash
npx drakov -f api.apib -p 3000
\`\`\`
*(Server sẽ bắt đầu lắng nghe tại `http://localhost:3000`)*

**Bước 2: Chạy Test tự động (Terminal 2)**
Giữ nguyên Terminal 1, mở một Terminal mới và dùng công cụ `dredd`. Dredd sẽ đọc file tài liệu để tự sinh ra kịch bản test, bắn request vào Mock Server và đối chiếu kết quả.
\`\`\`bash
npx dredd api.apib http://localhost:3000
\`\`\`

*(Kết quả mong đợi: `2 passing` - xác nhận các API GET và POST đều tuân thủ đúng "hợp đồng" tài liệu).*