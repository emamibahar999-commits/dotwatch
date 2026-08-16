const { pool } = require('../config/database');

exports.getPageTexts = async (req, res, next) => {
  try {
    const [rows] = await pool.execute('SELECT * FROM page_texts');
    const result = {};
    rows.forEach(r => {
      if (!result[r.section]) result[r.section] = {};
      result[r.section][r.key_name] = r.value;
    });
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.getPageTextBySection = async (req, res, next) => {
  try {
    const [rows] = await pool.execute('SELECT * FROM page_texts WHERE section = ?', [req.params.section]);
    const result = {};
    rows.forEach(r => result[r.key_name] = r.value);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.updatePageText = async (req, res, next) => {
  try {
    const { section, key_name, value } = req.body;
    await pool.execute(
      `INSERT INTO page_texts (section, key_name, value) VALUES (?,?,?) 
       ON DUPLICATE KEY UPDATE value = ?`,
      [section, key_name, value, value]
    );
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};
