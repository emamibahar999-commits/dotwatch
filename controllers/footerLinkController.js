const { pool } = require('../config/database');
const { buildUpdateSets } = require('../utils/helpers');

const ALLOWED_COLS = ['title', 'link', 'sort_order', 'active'];

exports.getFooterLinks = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      'SELECT * FROM footer_links WHERE active = 1 ORDER BY sort_order'
    );
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.createFooterLink = async (req, res, next) => {
  try {
    const { title, link, sort_order } = req.body;
    const [result] = await pool.execute(
      'INSERT INTO footer_links (title, link, sort_order) VALUES (?,?,?)',
      [title, link, sort_order || 0]
    );
    res.status(201).json({ id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateFooterLink = async (req, res, next) => {
  try {
    const { sets, vals } = buildUpdateSets(ALLOWED_COLS, req.body);
    if (!sets.length) return res.status(400).json({ error: 'No valid fields' });
    vals.push(req.params.id);
    await pool.execute(`UPDATE footer_links SET ${sets.join(',')} WHERE id = ?`, vals);
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};

exports.deleteFooterLink = async (req, res, next) => {
  try {
    await pool.execute('DELETE FROM footer_links WHERE id = ?', [req.params.id]);
    res.json({ deleted: true });
  } catch (err) {
    next(err);
  }
};
