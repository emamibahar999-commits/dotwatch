const express = require('express');
const router = express.Router();
const controller = require('../controllers/bannerController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');

router.get('/', controller.getBanners);
router.post('/', authenticate, adminOnly, controller.createBanner);
router.put('/:id', authenticate, adminOnly, controller.updateBanner);
router.delete('/:id', authenticate, adminOnly, controller.deleteBanner);

module.exports = router;
