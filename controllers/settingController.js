const { pool } = require('../config/database');
const { buildUpdateSets } = require('../utils/helpers');

const ALLOWED_COLS = [
  'store_name', 'store_email', 'store_phone', 'free_shipping_threshold',
  'maintenance_mode', 'allow_register', 'allow_reviews',
  'primary_color', 'secondary_color', 'bg_color', 'text_color', 'font_family'
];

exports.getSettings = async (req, res, next) => {
  try {
    const [rows] = await pool.execute('SELECT * FROM settings LIMIT 1');
    res.json(rows[0] || {});
  } catch (err) {
    next(err);
  }
};

exports.updateSettings = async (req, res, next) => {
  try {
    const { sets, vals } = buildUpdateSets(ALLOWED_COLS, req.body);
    if (!sets.length) return res.status(400).json({ error: 'No valid fields' });
    await pool.execute(`UPDATE settings SET ${sets.join(',')} WHERE id = 1`, vals);
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};
