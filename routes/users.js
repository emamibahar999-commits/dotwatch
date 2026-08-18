const express = require('express');
const router = express.Router();
const controller = require('../controllers/userController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');
const { userUpdateRules } = require('../utils/validators');

router.get('/', authenticate, adminOnly, controller.getUsers);
router.put('/:id', authenticate, adminOnly, userUpdateRules, controller.updateUser);

module.exports = router;
