# Buổi 11-12: API Design Patterns

## Kiến thức đạt được

### 1. Các mẫu thiết kế API phổ biến
- **CRUD (Create, Read, Update, Delete)**: Thường sử dụng các HTTP Methods (GET, POST, PUT, DELETE) map trực tiếp với các thao tác dữ liệu.
- **Query**: Sử dụng URL Parameters (ví dụ: `?category=Science&status=AVAILABLE`) để filter, sort, pagination dữ liệu trả về mà không thay đổi endpoint gốc.
- **HATEOAS (Hypermedia as the Engine of Application State)**: API trả về kèm theo các "links" điều hướng, giúp client biết được các actions tiếp theo có thể thực hiện tùy theo state hiện tại của resource (Ví dụ sách đang `AVAILABLE` thì có link `/borrow`, sách đang `BORROWED` thì có link `/return`).
- **Event-driven**: Hệ thống giao tiếp thông qua sự kiện. Phù hợp cho các xử lý bất đồng bộ (Asynchronous) như gửi email, push notification.
- **Webhook**: Cung cấp cơ chế "Reverse API". Thay vì client liên tục polling server, server sẽ gọi ngược lại client qua 1 URL cung cấp sẵn mỗi khi có event xảy ra.

### 2. Khi nào dùng REST, gRPC, GraphQL?

| Feature | REST | gRPC | GraphQL |
| :--- | :--- | :--- | :--- |
| **Giao thức** | HTTP/1.1 (thường dùng) | HTTP/2 | HTTP/1.1 hoặc HTTP/2 |
| **Định dạng dữ liệu** | JSON, XML | Protocol Buffers (Binary) | JSON |
| **Mô hình** | Resource-based | RPC (Hàm/Method-based) | Query-based |
| **Khi nào dùng?** | Public APIs, CRUD, các ứng dụng web thông thường. | Microservices nội bộ, cần hiệu năng cao, latency thấp, streaming. | Client cần tùy biến dữ liệu trả về (tránh over-fetching / under-fetching), aggregation từ nhiều nguồn. |

---

## Kỹ năng thực hành trong Demo

### 1. Thiết kế API dùng nhiều patterns kết hợp
Trong file `routes_books.py`, chúng ta đã kết hợp:
- **CRUD**: Cung cấp đầy đủ các endpoint để quản lý sách (GET, POST, PUT, DELETE).
- **Query**: Endpoint `GET /books?category=...&status=...` cho phép filter.
- **HATEOAS**: Khi lấy thông tin sách, response luôn kèm theo `_links` tự động thay đổi dựa trên state `AVAILABLE` hay `BORROWED`.

### 2. Triển khai Webhook và Event-driven
Trong file `routes_webhook.py`:
- Cung cấp endpoint `POST /webhooks/payment` giả lập việc nhận webhook từ Payment Gateway (như Stripe/VNPay).
- **Event-driven**: Nhận Webhook xong, thay vì gửi email báo cáo ngay (gây block), hệ thống push event vào Message Queue. Một Worker chạy ngầm sẽ lấy event ra và xử lý (gửi email), đảm bảo API phản hồi cực nhanh (<10ms).

---

## Phân tích API của Stripe và GitHub

### Stripe API
- **Chuẩn REST tuyệt đối**: URL phân cấp cực tốt dựa trên resource: `/v1/charges`, `/v1/customers`.
- **Webhook xuất sắc**: Stripe hỗ trợ webhook cho hầu hết mọi sự kiện. Họ cung cấp tính năng verify signature rất chặt chẽ, cùng với dashboard để xem log webhook lỗi/thành công và tính năng retry tự động.
- **Pagination**: Sử dụng pattern cursor-based pagination (chuyền `starting_after` hoặc `ending_before`) thay vì offset-based để đạt hiệu năng cao khi dữ liệu lớn.

### GitHub API
- **Hỗ trợ cả REST và GraphQL**: GitHub ban đầu thiết kế REST v3 cực kỳ chuẩn mực, áp dụng HATEOAS, pagination bằng header `Link`. Tuy nhiên, do data của GitHub rất chằng chịt (Issue -> Comments -> Users -> Repos), họ đã ra mắt **GraphQL v4** để giải quyết bài toán over-fetching/under-fetching.
- **Event-driven qua Webhook**: Hỗ trợ webhook mạnh mẽ ở mức độ Repository và Organization (ví dụ push code, tạo PR sẽ trigger webhook gọi tới CI/CD pipelines).

---

## Hướng dẫn chạy Demo

1. Cài đặt môi trường:
```bash
pip install flask
```

2. Chạy ứng dụng:
```bash
python app.py
```

3. Dùng Postman hoặc cURL để test các endpoint:
- **Lấy danh sách sách**: `GET http://localhost:5000/api/v1/books`
- **Mượn sách**: `POST http://localhost:5000/api/v1/books/B01/borrow`
- **Trả sách**: `POST http://localhost:5000/api/v1/books/B01/return`
- **Gửi giả lập Webhook**:
```bash
curl -X POST http://localhost:5000/api/v1/webhooks/payment \
-H "Content-Type: application/json" \
-d '{"event":"payment.success","data":{"user_id":"U01","amount":500000}}'
```
