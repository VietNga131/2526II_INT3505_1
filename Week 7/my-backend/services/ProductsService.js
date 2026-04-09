/* eslint-disable no-unused-vars */
const Service = require('./Service');
const Product = require('../models/Product'); // Nhúng Model vừa tạo

/**
* Lấy danh sách toàn bộ sản phẩm
**/
const productsGET = () => new Promise(
  async (resolve, reject) => {
    try {
      const items = await Product.find();
      resolve(Service.successResponse({ success: true, data: items }));
    } catch (e) {
      reject(Service.rejectResponse(e.message || 'Lỗi hệ thống', e.status || 500));
    }
  },
);

/**
* Xóa sản phẩm
**/
const productsIdDELETE = ({ id }) => new Promise(
  async (resolve, reject) => {
    try {
      const deleted = await Product.findByIdAndDelete(id);
      if (!deleted) throw new Error("Không tìm thấy sản phẩm");
      resolve(Service.successResponse({ message: "Xóa thành công" }));
    } catch (e) {
      reject(Service.rejectResponse(e.message || 'Lỗi hệ thống', e.status || 500));
    }
  },
);

/**
* Lấy chi tiết sản phẩm
**/
const productsIdGET = ({ id }) => new Promise(
  async (resolve, reject) => {
    try {
      const item = await Product.findById(id);
      if (!item) throw new Error("Không tìm thấy sản phẩm");
      resolve(Service.successResponse({ success: true, data: item }));
    } catch (e) {
      reject(Service.rejectResponse(e.message || 'Lỗi hệ thống', e.status || 500));
    }
  },
);

/**
* Cập nhật sản phẩm
**/
const productsIdPUT = ({ id, body }) => new Promise(
  async (resolve, reject) => {
    try {
      const updated = await Product.findByIdAndUpdate(id, body, { new: true });
      if (!updated) throw new Error("Không tìm thấy sản phẩm");
      resolve(Service.successResponse({ message: "Cập nhật thành công" }));
    } catch (e) {
      reject(Service.rejectResponse(e.message || 'Lỗi hệ thống', e.status || 500));
    }
  },
);

/**
* Thêm sản phẩm mới
**/
const productsPOST = ({ body }) => new Promise(
  async (resolve, reject) => {
    try {
      const newProduct = new Product(body);
      const saved = await newProduct.save();
      resolve(Service.successResponse({ success: true, data: saved }, 201));
    } catch (e) {
      reject(Service.rejectResponse(e.message || 'Lỗi hệ thống', e.status || 500));
    }
  },
);

module.exports = {
  productsGET,
  productsIdDELETE,
  productsIdGET,
  productsIdPUT,
  productsPOST,
};