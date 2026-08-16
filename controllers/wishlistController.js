const { pool } = require('../config/database');

exports.getWishlist = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      `SELECT w.id, w.product_id, p.name, b.nameFa as brandFa, p.price, p.image, p.status, p.deleted_at
       FROM wishlist w 
       JOIN products p ON w.product_id = p.id 
       LEFT JOIN brands b ON p.brand_id = b.id 
       WHERE w.user_id = ?`,
      [req.user.id]
    );
    const activeItems = rows.filter(r => r.status === 'active' && !r.deleted_at);
    res.json(activeItems);
  } catch (err) {
    next(err);
  }
};

exports.toggleWishlist = async (req, res, next) => {
  try {
    const { product_id } = req.body;

    const [existing] = await pool.execute(
      'SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?',
      [req.user.id, product_id]
    );

    if (existing.length) {
      await pool.execute(
        'DELETE FROM wishlist WHERE user_id = ? AND product_id = ?',
        [req.user.id, product_id]
      );
      return res.json({ removed: true });
    }

    const [products] = await pool.execute(
      'SELECT id FROM products WHERE id = ? AND status = "active" AND deleted_at IS NULL',
      [product_id]
    );
    if (!products.length) {
      return res.status(404).json({ error: 'Product not found' });
    }

    await pool.execute(
      'INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)',
      [req.user.id, product_id]
    );
    res.json({ added: true });
  } catch (err) {
    next(err);
  }
};

exports.removeFromWishlist = async (req, res, next) => {
  try {
    await pool.execute(
      'DELETE FROM wishlist WHERE user_id = ? AND product_id = ?',
      [req.user.id, req.params.product_id]
    );
    res.json({ deleted: true });
  } catch (err) {
    next(err);
  }
};
