const express = require('express');
const router = express.Router();
const controller = require('../controllers/authController');
const { authenticate } = require('../middleware/auth');
const { registerRules, loginRules } = require('../utils/validators');
const { authLimiter } = require('../middleware/rateLimiter');

router.post('/register', authLimiter, registerRules, controller.register);
router.post('/login', authLimiter, loginRules, controller.login);
router.get('/me', authenticate, controller.me);

module.exports = router;
