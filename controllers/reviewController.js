const { pool } = require('../config/database');

exports.getReviews = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      `SELECT r.id, r.rating, r.comment, r.created_at, u.name as user_name
       FROM reviews r 
       JOIN users u ON r.user_id = u.id 
       WHERE r.product_id = ? AND r.status = "approved"
       ORDER BY r.created_at DESC`,
      [req.params.id]
    );
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.createReview = async (req, res, next) => {
  try {
    const { rating, comment } = req.body;
    const product_id = req.params.id;

    const [purchases] = await pool.execute(
      `SELECT DISTINCT oi.product_id 
       FROM orders o 
       JOIN order_items oi ON o.id = oi.order_id 
       WHERE o.user_id = ? AND oi.product_id = ? AND o.status != "cancelled"`,
      [req.user.id, product_id]
    );

    if (!purchases.length) {
      return res.status(403).json({ error: 'You can only review products you have purchased' });
    }

    const [existing] = await pool.execute(
      'SELECT id FROM reviews WHERE user_id = ? AND product_id = ?',
      [req.user.id, product_id]
    );
    if (existing.length) {
      return res.status(409).json({ error: 'You have already reviewed this product' });
    }

    await pool.execute(
      'INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (?, ?, ?, ?)',
      [req.user.id, product_id, rating, comment || null]
    );
    res.status(201).json({ submitted: true });
  } catch (err) {
    next(err);
  }
};
