const express = require('express');
const router = express.Router();
const controller = require('../controllers/addressController');
const { authenticate } = require('../middleware/auth');

router.get('/', authenticate, controller.getAddresses);
router.post('/', authenticate, controller.createAddress);
router.put('/:id', authenticate, controller.updateAddress);
router.delete('/:id', authenticate, controller.deleteAddress);

module.exports = router;
