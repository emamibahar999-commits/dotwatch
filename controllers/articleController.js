const { pool } = require('../config/database');

exports.getArticles = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      `SELECT id, title, category, author, image, excerpt, created_at 
       FROM articles WHERE status = "published" AND deleted_at IS NULL 
       ORDER BY created_at DESC`
    );
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.getArticle = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      'SELECT * FROM articles WHERE id = ? AND status = "published" AND deleted_at IS NULL',
      [req.params.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Article not found' });
    await pool.execute('UPDATE articles SET views = views + 1 WHERE id = ?', [req.params.id]);
    res.json(rows[0]);
  } catch (err) {
    next(err);
  }
};
