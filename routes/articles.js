const express = require('express');
const router = express.Router();
const controller = require('../controllers/articleController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');

router.get('/', controller.getArticles);
router.get('/:id', controller.getArticle);

module.exports = router;
