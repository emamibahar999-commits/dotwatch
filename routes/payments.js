const express = require('express');
const router = express.Router();
const controller = require('../controllers/paymentController');
const { authenticate } = require('../middleware/auth');

router.post('/request', authenticate, controller.requestPayment);
router.get('/verify', controller.verifyPayment);

module.exports = router;
