const express = require('express');
const router = express.Router();
const controller = require('../controllers/menuController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');

router.get('/', controller.getMenus);
router.post('/', authenticate, adminOnly, controller.createMenu);
router.put('/:id', authenticate, adminOnly, controller.updateMenu);
router.delete('/:id', authenticate, adminOnly, controller.deleteMenu);

module.exports = router;
