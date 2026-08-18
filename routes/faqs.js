const express = require('express');
const router = express.Router();
const controller = require('../controllers/faqController');

router.get('/', controller.getFaqs);

module.exports = router;
