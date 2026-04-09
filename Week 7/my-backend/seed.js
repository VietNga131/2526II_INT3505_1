const mongoose = require('mongoose');
const Product = require('./models/Product'); // Nhúng Model của bạn

// Danh sách dữ liệu mẫu bạn muốn thêm vào
const sampleProducts = [
  { name: "Laptop Dell XPS 15", price: 1500, category: "Electronics" },
  { name: "MacBook Pro M2", price: 2000, category: "Electronics" },
  { name: "Bàn phím cơ Keychron K8", price: 100, category: "Accessories" },
  { name: "Chuột Logitech MX Master 3S", price: 120, category: "Accessories" },
  { name: "Màn hình LG UltraFine 4K", price: 600, category: "Electronics" },
  { name: "Balo chống nước The North Face", price: 50, category: "Fashion" },
  { name: "Tai nghe Sony WH-1000XM5", price: 350, category: "Electronics" }
];

// Mở kết nối tới Database (Đổi thành localhost nếu máy bạn đang dùng localhost)
mongoose.connect('mongodb://localhost:27017/product_management')
  .then(async () => {
    console.log('⏳ Đang kết nối MongoDB để tạo dữ liệu mẫu...');

    // (Tùy chọn) Xóa sạch dữ liệu cũ để tránh bị trùng lặp khi chạy nhiều lần
    await Product.deleteMany({});
    console.log('🧹 Đã dọn dẹp dữ liệu cũ!');

    // Bơm toàn bộ mảng dữ liệu mẫu vào DB
    await Product.insertMany(sampleProducts);
    console.log(`🎉 Đã thêm thành công ${sampleProducts.length} sản phẩm mẫu!`);

    // Thêm xong thì đóng kết nối lại
    mongoose.connection.close();
  })
  .catch(err => {
    console.error('❌ Lỗi:', err);
    mongoose.connection.close();
  });