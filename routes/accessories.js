const express = require('express');
const router = express.Router();
const controller = require('../controllers/accessoryController');

router.get('/', controller.getAccessories);

module.exports = router;
