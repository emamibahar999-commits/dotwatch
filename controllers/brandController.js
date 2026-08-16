const { pool } = require('../config/database');

exports.getBrands = async (req, res, next) => {
  try {
    const [rows] = await pool.execute('SELECT * FROM brands WHERE deleted_at IS NULL ORDER BY nameFa');
    res.json(rows);
  } catch (err) {
    next(err);
  }
};
