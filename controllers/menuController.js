const { pool } = require('../config/database');
const { buildUpdateSets } = require('../utils/helpers');

const ALLOWED_COLS = ['title', 'link', 'icon', 'parent_id', 'sort_order', 'active'];

exports.getMenus = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      'SELECT * FROM menus WHERE active = 1 ORDER BY sort_order'
    );
    const parents = rows.filter(m => !m.parent_id);
    const result = parents.map(p => ({ ...p, submenu: rows.filter(c => c.parent_id === p.id) }));
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.createMenu = async (req, res, next) => {
  try {
    const { title, link, icon, parent_id, sort_order } = req.body;
    const [result] = await pool.execute(
      'INSERT INTO menus (title, link, icon, parent_id, sort_order) VALUES (?,?,?,?,?)',
      [title, link, icon, parent_id || null, sort_order || 0]
    );
    res.status(201).json({ id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateMenu = async (req, res, next) => {
  try {
    const { sets, vals } = buildUpdateSets(ALLOWED_COLS, req.body);
    if (!sets.length) return res.status(400).json({ error: 'No valid fields' });
    vals.push(req.params.id);
    await pool.execute(`UPDATE menus SET ${sets.join(',')} WHERE id = ?`, vals);
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};

exports.deleteMenu = async (req, res, next) => {
  try {
    await pool.execute('DELETE FROM menus WHERE id = ?', [req.params.id]);
    res.json({ deleted: true });
  } catch (err) {
    next(err);
  }
};
