const express = require('express');
const router = express.Router();
const controller = require('../controllers/pageTextController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');

router.get('/', controller.getPageTexts);
router.get('/:section', controller.getPageTextBySection);
router.put('/', authenticate, adminOnly, controller.updatePageText);

module.exports = router;
