const { pool } = require('../config/database');

exports.getCart = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      `SELECT c.id, c.product_id, c.qty, p.name, p.brand_id, b.nameFa as brandFa, 
              p.price, p.image, p.stock, p.status, p.deleted_at
       FROM cart_items c 
       JOIN products p ON c.product_id = p.id 
       LEFT JOIN brands b ON p.brand_id = b.id 
       WHERE c.user_id = ? AND p.status = "active" AND p.deleted_at IS NULL`,
      [req.user.id]
    );
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.addToCart = async (req, res, next) => {
  try {
    const { product_id, qty = 1 } = req.body;
    const quantity = Math.max(1, parseInt(qty) || 1);

    const [products] = await pool.execute(
      'SELECT stock, status, deleted_at FROM products WHERE id = ? AND deleted_at IS NULL',
      [product_id]
    );
    if (!products.length || products[0].status !== 'active' || products[0].deleted_at) {
      return res.status(404).json({ error: 'Product not found or unavailable' });
    }

    const [cartItems] = await pool.execute(
      'SELECT qty FROM cart_items WHERE user_id = ? AND product_id = ?',
      [req.user.id, product_id]
    );
    const currentQty = cartItems.length ? cartItems[0].qty : 0;
    const newTotalQty = currentQty + quantity;

    if (newTotalQty > products[0].stock) {
      return res.status(400).json({ 
        error: 'Insufficient stock', 
        available: products[0].stock,
        requested: newTotalQty 
      });
    }

    await pool.execute(
      `INSERT INTO cart_items (user_id, product_id, qty) VALUES (?, ?, ?) 
       ON DUPLICATE KEY UPDATE qty = qty + ?`,
      [req.user.id, product_id, quantity, quantity]
    );
    res.json({ added: true });
  } catch (err) {
    next(err);
  }
};

exports.updateCart = async (req, res, next) => {
  try {
    const product_id = req.params.product_id;
    const qty = parseInt(req.body.qty) || 0;

    if (qty <= 0) {
      await pool.execute(
        'DELETE FROM cart_items WHERE user_id = ? AND product_id = ?',
        [req.user.id, product_id]
      );
      return res.json({ updated: true, removed: true });
    }

    const [products] = await pool.execute(
      'SELECT stock FROM products WHERE id = ? AND status = "active" AND deleted_at IS NULL',
      [product_id]
    );
    if (!products.length) {
      return res.status(404).json({ error: 'Product not found' });
    }
    if (qty > products[0].stock) {
      return res.status(400).json({ 
        error: 'Insufficient stock', 
        available: products[0].stock 
      });
    }

    await pool.execute(
      'UPDATE cart_items SET qty = ? WHERE user_id = ? AND product_id = ?',
      [qty, req.user.id, product_id]
    );
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};

exports.removeFromCart = async (req, res, next) => {
  try {
    await pool.execute(
      'DELETE FROM cart_items WHERE user_id = ? AND product_id = ?',
      [req.user.id, req.params.product_id]
    );
    res.json({ deleted: true });
  } catch (err) {
    next(err);
  }
};
