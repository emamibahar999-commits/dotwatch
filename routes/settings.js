const express = require('express');
const router = express.Router();
const controller = require('../controllers/settingController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');

router.get('/', controller.getSettings);
router.put('/', authenticate, adminOnly, controller.updateSettings);

module.exports = router;
