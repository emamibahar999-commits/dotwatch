const { pool } = require('../config/database');

exports.getAddresses = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      'SELECT * FROM addresses WHERE user_id = ? ORDER BY is_default DESC, created_at DESC',
      [req.user.id]
    );
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.createAddress = async (req, res, next) => {
  try {
    const { title, city, address, postal_code, phone, is_default } = req.body;
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      if (is_default) {
        await conn.execute(
          'UPDATE addresses SET is_default = 0 WHERE user_id = ?',
          [req.user.id]
        );
      }
      const [result] = await conn.execute(
        'INSERT INTO addresses (user_id, title, city, address, postal_code, phone, is_default) VALUES (?,?,?,?,?,?,?)',
        [req.user.id, title, city, address, postal_code || null, phone || null, is_default ? 1 : 0]
      );
      await conn.commit();
      res.status(201).json({ id: result.insertId });
    } catch (err) {
      await conn.rollback();
      throw err;
    } finally {
      conn.release();
    }
  } catch (err) {
    next(err);
  }
};

exports.updateAddress = async (req, res, next) => {
  try {
    const { title, city, address, postal_code, phone, is_default } = req.body;
    const [existing] = await pool.execute(
      'SELECT id FROM addresses WHERE id = ? AND user_id = ?',
      [req.params.id, req.user.id]
    );
    if (!existing.length) return res.status(404).json({ error: 'Address not found' });

    const fields = [];
    const vals = [];
    if (title !== undefined) { fields.push('title = ?'); vals.push(title); }
    if (city !== undefined) { fields.push('city = ?'); vals.push(city); }
    if (address !== undefined) { fields.push('address = ?'); vals.push(address); }
    if (postal_code !== undefined) { fields.push('postal_code = ?'); vals.push(postal_code); }
    if (phone !== undefined) { fields.push('phone = ?'); vals.push(phone); }
    if (is_default !== undefined) { fields.push('is_default = ?'); vals.push(is_default ? 1 : 0); }
    vals.push(req.params.id);

    await pool.execute(
      `UPDATE addresses SET ${fields.join(',')} WHERE id = ?`,
      vals
    );
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};

exports.deleteAddress = async (req, res, next) => {
  try {
    await pool.execute(
      'DELETE FROM addresses WHERE id = ? AND user_id = ?',
      [req.params.id, req.user.id]
    );
    res.json({ deleted: true });
  } catch (err) {
    next(err);
  }
};
