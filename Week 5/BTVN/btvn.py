import sqlite3
import time

# 1. Khởi tạo Database và tạo 1 triệu bản ghi
conn = sqlite3.connect(':memory:') # Chạy trên RAM để thấy rõ sự khác biệt xử lý của CPU
cursor = conn.cursor()
cursor.execute('CREATE TABLE readers (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')

print("Đang tạo 1 triệu bản ghi... vui lòng chờ...")
data = [(i, f"User {i}", f"user{i}@example.com") for i in range(1, 1000001)]
cursor.executemany('INSERT INTO readers VALUES (?, ?, ?)', data)
conn.commit()
print("Đã tạo xong!")

# Cấu hình thử nghiệm
limit = 10
target_offset = 999900  # Lấy 10 bản ghi cuối cùng

# --- PHƯƠNG PHÁP 1: OFFSET-BASED (PAGE-BASED) ---
start_time = time.time()
cursor.execute(f'SELECT * FROM readers LIMIT {limit} OFFSET {target_offset}')
results_offset = cursor.fetchall()
offset_time = time.time() - start_time

# --- PHƯƠNG PHÁP 2: CURSOR-BASED ---
# Giả sử chúng ta đã biết ID trước đó (cursor) là 999900
cursor_id = 999900
start_time = time.time()
cursor.execute(f'SELECT * FROM readers WHERE id > {cursor_id} LIMIT {limit}')
results_cursor = cursor.fetchall()
cursor_time = time.time() - start_time

# 2. Hiển thị kết quả
print("\n" + "="*40)
print(f"{'Phương pháp':<20} | {'Thời gian thực thi (s)':<20}")
print("-" * 40)
print(f"{'Offset-based':<20} | {offset_time:.6f}s")
print(f"{'Cursor-based':<20} | {cursor_time:.6f}s")
print("="*40)

speed_diff = offset_time / cursor_time if cursor_time > 0 else 0
print(f"\n=> Cursor-based nhanh gấp khoảng {speed_diff:.1f} lần!")