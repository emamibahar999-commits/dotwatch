const express = require('express');
const router = express.Router();
const controller = require('../controllers/orderController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');
const { orderRules } = require('../utils/validators');

router.get('/', authenticate, controller.getOrders);
router.get('/:id', authenticate, controller.getOrder);
router.post('/', authenticate, orderRules, controller.createOrder);
router.put('/:id/status', authenticate, adminOnly, controller.updateOrderStatus);

module.exports = router;
