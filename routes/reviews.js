const express = require('express');
const router = express.Router();
const controller = require('../controllers/reviewController');
const { authenticate } = require('../middleware/auth');
const { reviewRules } = require('../utils/validators');

router.get('/products/:id/reviews', controller.getReviews);
router.post('/products/:id/reviews', authenticate, reviewRules, controller.createReview);

module.exports = router;
