const config = require('./config');
const logger = require('./logger');
const ExpressServer = require('./expressServer');
const mongoose = require('mongoose'); // Thêm dòng này

// --- THÊM ĐOẠN KẾT NỐI MONGODB VÀO ĐÂY ---
mongoose.connect('mongodb://localhost:27017/product_management')
  .then(() => logger.info('✅ Đã kết nối thành công tới MongoDB!'))
  .catch(err => logger.error('❌ Lỗi kết nối MongoDB:', err));
// ----------------------------------------

const launchServer = async () => {
  try {
    this.expressServer = new ExpressServer(config.URL_PORT, config.OPENAPI_YAML);
    this.expressServer.launch();
    logger.info('Express server running');
  } catch (error) {
    logger.error('Express Server failure', error.message);
    await this.close();
  }
};

launchServer().catch(e => logger.error(e));
