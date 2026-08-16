const { pool } = require('../config/database');

exports.getFaqs = async (req, res, next) => {
  try {
    const [rows] = await pool.execute('SELECT * FROM faqs ORDER BY sort_order');
    res.json(rows);
  } catch (err) {
    next(err);
  }
};
