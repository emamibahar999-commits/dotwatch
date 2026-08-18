const express = require('express');
const router = express.Router();
const controller = require('../controllers/brandController');

router.get('/', controller.getBrands);

module.exports = router;
