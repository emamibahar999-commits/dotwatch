const express = require('express');
const router = express.Router();
const controller = require('../controllers/wishlistController');
const { authenticate } = require('../middleware/auth');

router.get('/', authenticate, controller.getWishlist);
router.post('/', authenticate, controller.toggleWishlist);
router.delete('/:product_id', authenticate, controller.removeFromWishlist);

module.exports = router;
