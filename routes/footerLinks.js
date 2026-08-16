const express = require('express');
const router = express.Router();
const controller = require('../controllers/footerLinkController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');

router.get('/', controller.getFooterLinks);
router.post('/', authenticate, adminOnly, controller.createFooterLink);
router.put('/:id', authenticate, adminOnly, controller.updateFooterLink);
router.delete('/:id', authenticate, adminOnly, controller.deleteFooterLink);

module.exports = router;
