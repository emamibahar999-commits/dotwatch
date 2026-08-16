const { pool } = require('../config/database');
const { buildUpdateSets } = require('../utils/helpers');

const ALLOWED_COLS = ['title', 'subtitle', 'image', 'link', 'position', 'sort_order', 'active'];

exports.getBanners = async (req, res, next) => {
  try {
    const { position } = req.query;
    let sql = 'SELECT * FROM banners WHERE active = 1';
    const params = [];
    if (position) { sql += ' AND position = ?'; params.push(position); }
    sql += ' ORDER BY sort_order';
    const [rows] = await pool.execute(sql, params);
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.createBanner = async (req, res, next) => {
  try {
    const { title, subtitle, image, link, position, sort_order } = req.body;
    const [result] = await pool.execute(
      'INSERT INTO banners (title, subtitle, image, link, position, sort_order) VALUES (?,?,?,?,?,?)',
      [title, subtitle, image, link, position || 'main', sort_order || 0]
    );
    res.status(201).json({ id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateBanner = async (req, res, next) => {
  try {
    const { sets, vals } = buildUpdateSets(ALLOWED_COLS, req.body);
    if (!sets.length) return res.status(400).json({ error: 'No valid fields' });
    vals.push(req.params.id);
    await pool.execute(`UPDATE banners SET ${sets.join(',')} WHERE id = ?`, vals);
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};

exports.deleteBanner = async (req, res, next) => {
  try {
    await pool.execute('DELETE FROM banners WHERE id = ?', [req.params.id]);
    res.json({ deleted: true });
  } catch (err) {
    next(err);
  }
};
