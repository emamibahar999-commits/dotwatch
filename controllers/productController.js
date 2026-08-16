const { pool } = require('../config/database');
const { sanitizeColumns, buildUpdateSets } = require('../utils/helpers');

const ALLOWED_PRODUCT_COLS = [
  'name', 'brand_id', 'price', 'old_price', 'discount', 'gender', 'style', 'type',
  'material', 'color', 'image', 'rating', 'reviews', 'is_new', 'stock',
  'movement', 'diameter', 'thickness', 'case_material', 'band_material',
  'glass', 'water_resistant', 'weight', 'functions', 'features', 'description', 'status'
];

exports.listProducts = async (req, res, next) => {
  try {
    const {
      gender, style, type, material, color, brand,
      minPrice, maxPrice, sort, search, limit = 50, page = 1
    } = req.query;

    let sql = `SELECT p.*, b.nameFa as brandFa 
               FROM products p 
               LEFT JOIN brands b ON p.brand_id = b.id 
               WHERE p.status = "active" AND p.deleted_at IS NULL`;
    const params = [];

    if (gender) { sql += ' AND p.gender = ?'; params.push(gender); }
    if (style) { sql += ' AND p.style = ?'; params.push(style); }
    if (type) { sql += ' AND p.type = ?'; params.push(type); }
    if (material) { sql += ' AND p.material = ?'; params.push(material); }
    if (color) { sql += ' AND p.color = ?'; params.push(color); }
    if (brand) { sql += ' AND b.name = ?'; params.push(brand); }
    if (minPrice) { sql += ' AND p.price >= ?'; params.push(Number(minPrice)); }
    if (maxPrice) { sql += ' AND p.price <= ?'; params.push(Number(maxPrice)); }
    if (search) {
      sql += ' AND (p.name LIKE ? OR b.nameFa LIKE ?)';
      params.push(`%${search}%`, `%${search}%`);
    }

    if (sort === 'price-asc') sql += ' ORDER BY p.price ASC';
    else if (sort === 'price-desc') sql += ' ORDER BY p.price DESC';
    else if (sort === 'newest') sql += ' ORDER BY p.is_new DESC, p.created_at DESC';
    else if (sort === 'discount') sql += ' ORDER BY p.discount DESC';
    else sql += ' ORDER BY p.rating DESC';

    const pageNum = Math.max(1, parseInt(page) || 1);
    const limitNum = Math.min(100, Math.max(1, parseInt(limit) || 50));
    sql += ' LIMIT ? OFFSET ?';
    params.push(limitNum, (pageNum - 1) * limitNum);

    const [rows] = await pool.execute(sql, params);
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.getProduct = async (req, res, next) => {
  try {
    const [rows] = await pool.execute(
      `SELECT p.*, b.nameFa as brandFa 
       FROM products p 
       LEFT JOIN brands b ON p.brand_id = b.id 
       WHERE p.id = ? AND p.status = "active" AND p.deleted_at IS NULL`,
      [req.params.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Product not found' });
    res.json(rows[0]);
  } catch (err) {
    next(err);
  }
};

exports.createProduct = async (req, res, next) => {
  try {
    const { cols, vals } = sanitizeColumns(ALLOWED_PRODUCT_COLS, req.body);
    if (!cols.length) {
      return res.status(400).json({ error: 'No valid fields provided' });
    }
    const [result] = await pool.execute(
      `INSERT INTO products (${cols.join(',')}) VALUES (${cols.map(() => '?').join(',')})`,
      vals
    );
    res.status(201).json({ id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateProduct = async (req, res, next) => {
  try {
    const { sets, vals } = buildUpdateSets(ALLOWED_PRODUCT_COLS, req.body);
    if (!sets.length) {
      return res.status(400).json({ error: 'No valid fields provided' });
    }
    vals.push(req.params.id);
    const [result] = await pool.execute(
      `UPDATE products SET ${sets.join(',')} WHERE id = ? AND deleted_at IS NULL`,
      vals
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};

exports.deleteProduct = async (req, res, next) => {
  try {
    const [result] = await pool.execute(
      'UPDATE products SET status = "inactive", deleted_at = NOW() WHERE id = ? AND deleted_at IS NULL',
      [req.params.id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    res.json({ deleted: true });
  } catch (err) {
    next(err);
  }
};
