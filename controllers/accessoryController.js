const { pool } = require('../config/database');

exports.getAccessories = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      'SELECT * FROM accessories WHERE status = "active" AND deleted_at IS NULL'
    );
    res.json(rows);
  } catch (err) {
    next(err);
  }
};
