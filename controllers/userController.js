const { pool } = require('../config/database');

exports.getUsers = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      'SELECT id, name, email, phone, role, status, created_at FROM users WHERE deleted_at IS NULL'
    );
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.updateUser = async (req, res, next) => {
  try {
    const { status, role } = req.body;
    const fields = [];
    const vals = [];
    if (status !== undefined) { fields.push('status = ?'); vals.push(status); }
    if (role !== undefined) { fields.push('role = ?'); vals.push(role); }
    if (!fields.length) return res.status(400).json({ error: 'No valid fields' });
    vals.push(req.params.id);
    await pool.execute(
      `UPDATE users SET ${fields.join(',')} WHERE id = ? AND deleted_at IS NULL`,
      vals
    );
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};
