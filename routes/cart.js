const express = require('express');
const router = express.Router();
const controller = require('../controllers/cartController');
const { authenticate } = require('../middleware/auth');
const { cartRules, cartUpdateRules } = require('../utils/validators');

router.get('/', authenticate, controller.getCart);
router.post('/', authenticate, cartRules, controller.addToCart);
router.put('/:product_id', authenticate, cartUpdateRules, controller.updateCart);
router.delete('/:product_id', authenticate, controller.removeFromCart);

module.exports = router;
