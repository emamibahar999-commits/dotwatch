const express = require('express');
const router = express.Router();
const controller = require('../controllers/adminController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');

router.get('/stats', authenticate, adminOnly, controller.getStats);
router.get('/data', authenticate, adminOnly, controller.getFullData);
router.get('/backup', authenticate, adminOnly, controller.getBackup);

module.exports = router;
