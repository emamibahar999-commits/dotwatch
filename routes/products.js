const express = require('express');
const router = express.Router();
const controller = require('../controllers/productController');
const { authenticate } = require('../middleware/auth');
const { adminOnly } = require('../middleware/admin');
const { productCreateRules } = require('../utils/validators');

router.get('/', controller.listProducts);
router.get('/:id', controller.getProduct);
router.post('/', authenticate, adminOnly, productCreateRules, controller.createProduct);
router.put('/:id', authenticate, adminOnly, productCreateRules, controller.updateProduct);
router.delete('/:id', authenticate, adminOnly, controller.deleteProduct);

module.exports = router;
