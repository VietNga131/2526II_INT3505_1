const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  category: { type: String, default: "General" }
});

// Hàm này giúp đổi '_id' mặc định của MongoDB thành 'id' để khớp với chuẩn OpenAPI của bạn
ProductSchema.method("toJSON", function() {
  const { __v, _id, ...object } = this.toObject();
  object.id = _id;
  return object;
});

module.exports = mongoose.model('Product', ProductSchema);