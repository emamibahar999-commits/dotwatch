const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// ========== DB Config ==========
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASS || '',
  database: process.env.DB_NAME || 'dotwatch',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  charset: 'utf8mb4'
};

const pool = mysql.createPool(dbConfig);

// ========== Helpers ==========
const JWT_SECRET = process.env.JWT_SECRET || 'dotwatch_secret_key_2026';
const auth = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch { res.status(401).json({ error: 'Invalid token' }); }
};
const adminOnly = (req, res, next) => {
  if (req.user.role !== 'admin') return res.status(403).json({ error: 'Admin only' });
  next();
};
const genOrderNum = () => 'DW-' + Date.now().toString(36).toUpperCase();

// ========== AUTH ==========
app.post('/api/auth/register', async (req, res) => {
  const { name, email, phone, password } = req.body;
  if (!name || !email || !password) return res.status(400).json({ error: 'Name, email, password required' });
  try {
    const [exist] = await pool.execute('SELECT id FROM users WHERE email=?', [email]);
    if (exist.length) return res.status(409).json({ error: 'Email already exists' });
    const hash = await bcrypt.hash(password, 10);
    const [r] = await pool.execute('INSERT INTO users (name, email, phone, password_hash) VALUES (?,?,?,?)', [name, email, phone || null, hash]);
    const token = jwt.sign({ id: r.insertId, email, role: 'user' }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: r.insertId, name, email, phone, role: 'user' } });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const [rows] = await pool.execute('SELECT * FROM users WHERE email=? AND status="active"', [email]);
    if (!rows.length) return res.status(401).json({ error: 'Invalid credentials' });
    const user = rows[0];
    const ok = await bcrypt.compare(password, user.password_hash);
    if (!ok) return res.status(401).json({ error: 'Invalid credentials' });
    const token = jwt.sign({ id: user.id, email: user.email, role: user.role }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user.id, name: user.name, email: user.email, phone: user.phone, role: user.role, avatar: user.avatar } });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/auth/me', auth, async (req, res) => {
  const [rows] = await pool.execute('SELECT id,name,email,phone,avatar,role FROM users WHERE id=?', [req.user.id]);
  res.json(rows[0] || {});
});

// ========== PRODUCTS ==========
app.get('/api/products', async (req, res) => {
  const { gender, style, type, material, color, brand, minPrice, maxPrice, sort, search, limit = 50, page = 1 } = req.query;
  let sql = 'SELECT p.*, b.nameFa as brandFa FROM products p LEFT JOIN brands b ON p.brand_id=b.id WHERE p.status="active"';
  const params = [];
  if (gender) { sql += ' AND p.gender=?'; params.push(gender); }
  if (style) { sql += ' AND p.style=?'; params.push(style); }
  if (type) { sql += ' AND p.type=?'; params.push(type); }
  if (material) { sql += ' AND p.material=?'; params.push(material); }
  if (color) { sql += ' AND p.color=?'; params.push(color); }
  if (brand) { sql += ' AND b.name=?'; params.push(brand); }
  if (minPrice) { sql += ' AND p.price>=?'; params.push(minPrice); }
  if (maxPrice) { sql += ' AND p.price<=?'; params.push(maxPrice); }
  if (search) { sql += ' AND (p.name LIKE ? OR b.nameFa LIKE ?)'; params.push(`%${search}%`, `%${search}%`); }
  if (sort === 'price-asc') sql += ' ORDER BY p.price ASC';
  else if (sort === 'price-desc') sql += ' ORDER BY p.price DESC';
  else if (sort === 'newest') sql += ' ORDER BY p.is_new DESC, p.created_at DESC';
  else if (sort === 'discount') sql += ' ORDER BY p.discount DESC';
  else sql += ' ORDER BY p.rating DESC';
  sql += ' LIMIT ? OFFSET ?'; params.push(parseInt(limit), (parseInt(page)-1)*parseInt(limit));
  const [rows] = await pool.execute(sql, params);
  res.json(rows);
});

app.get('/api/products/:id', async (req, res) => {
  const [rows] = await pool.execute('SELECT p.*, b.nameFa as brandFa FROM products p LEFT JOIN brands b ON p.brand_id=b.id WHERE p.id=?', [req.params.id]);
  if (!rows.length) return res.status(404).json({ error: 'Not found' });
  res.json(rows[0]);
});

app.post('/api/products', auth, adminOnly, async (req, res) => {
  const fields = req.body;
  const cols = Object.keys(fields).join(',');
  const vals = Object.values(fields);
  const ph = vals.map(()=>'?').join(',');
  const [r] = await pool.execute(`INSERT INTO products (${cols}) VALUES (${ph})`, vals);
  res.json({ id: r.insertId });
});

app.put('/api/products/:id', auth, adminOnly, async (req, res) => {
  const fields = req.body;
  const sets = Object.keys(fields).map(k=>`${k}=?`).join(',');
  const vals = [...Object.values(fields), req.params.id];
  await pool.execute(`UPDATE products SET ${sets} WHERE id=?`, vals);
  res.json({ updated: true });
});

app.delete('/api/products/:id', auth, adminOnly, async (req, res) => {
  await pool.execute('UPDATE products SET status="inactive" WHERE id=?', [req.params.id]);
  res.json({ deleted: true });
});

// ========== BRANDS ==========
app.get('/api/brands', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM brands ORDER BY nameFa');
  res.json(rows);
});

// ========== ACCESSORIES ==========
app.get('/api/accessories', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM accessories WHERE status="active"');
  res.json(rows);
});

// ========== ARTICLES ==========
app.get('/api/articles', async (req, res) => {
  const [rows] = await pool.execute('SELECT id,title,category,author,image,excerpt,created_at FROM articles WHERE status="published" ORDER BY created_at DESC');
  res.json(rows);
});

app.get('/api/articles/:id', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM articles WHERE id=? AND status="published"', [req.params.id]);
  if (!rows.length) return res.status(404).json({ error: 'Not found' });
  await pool.execute('UPDATE articles SET views=views+1 WHERE id=?', [req.params.id]);
  res.json(rows[0]);
});

// ========== FAQS ==========
app.get('/api/faqs', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM faqs ORDER BY sort_order');
  res.json(rows);
});

// ========== CART ==========
app.get('/api/cart', auth, async (req, res) => {
  const [rows] = await pool.execute(`SELECT c.*, p.name, p.brand_id, b.nameFa as brandFa, p.price, p.image, p.stock 
    FROM cart_items c JOIN products p ON c.product_id=p.id LEFT JOIN brands b ON p.brand_id=b.id WHERE c.user_id=?`, [req.user.id]);
  res.json(rows);
});

app.post('/api/cart', auth, async (req, res) => {
  const { product_id, qty = 1 } = req.body;
  await pool.execute('INSERT INTO cart_items (user_id, product_id, qty) VALUES (?,?,?) ON DUPLICATE KEY UPDATE qty=qty+?', [req.user.id, product_id, qty, qty]);
  res.json({ added: true });
});

app.put('/api/cart/:product_id', auth, async (req, res) => {
  const { qty } = req.body;
  if (qty <= 0) {
    await pool.execute('DELETE FROM cart_items WHERE user_id=? AND product_id=?', [req.user.id, req.params.product_id]);
  } else {
    await pool.execute('UPDATE cart_items SET qty=? WHERE user_id=? AND product_id=?', [qty, req.user.id, req.params.product_id]);
  }
  res.json({ updated: true });
});

app.delete('/api/cart/:product_id', auth, async (req, res) => {
  await pool.execute('DELETE FROM cart_items WHERE user_id=? AND product_id=?', [req.user.id, req.params.product_id]);
  res.json({ deleted: true });
});

// ========== WISHLIST ==========
app.get('/api/wishlist', auth, async (req, res) => {
  const [rows] = await pool.execute(`SELECT w.*, p.name, b.nameFa as brandFa, p.price, p.image 
    FROM wishlist w JOIN products p ON w.product_id=p.id LEFT JOIN brands b ON p.brand_id=b.id WHERE w.user_id=?`, [req.user.id]);
  res.json(rows);
});

app.post('/api/wishlist', auth, async (req, res) => {
  const { product_id } = req.body;
  try {
    await pool.execute('INSERT INTO wishlist (user_id, product_id) VALUES (?,?)', [req.user.id, product_id]);
    res.json({ added: true });
  } catch { res.json({ removed: true }); }
});

app.delete('/api/wishlist/:product_id', auth, async (req, res) => {
  await pool.execute('DELETE FROM wishlist WHERE user_id=? AND product_id=?', [req.user.id, req.params.product_id]);
  res.json({ deleted: true });
});

// ========== ORDERS ==========
app.get('/api/orders', auth, async (req, res) => {
  let sql = 'SELECT * FROM orders WHERE user_id=? ORDER BY created_at DESC';
  let params = [req.user.id];
  if (req.user.role === 'admin' && req.query.all === '1') { sql = 'SELECT * FROM orders ORDER BY created_at DESC'; params = []; }
  const [rows] = await pool.execute(sql, params);
  res.json(rows);
});

app.get('/api/orders/:id', auth, async (req, res) => {
  const [orders] = await pool.execute('SELECT * FROM orders WHERE id=?', [req.params.id]);
  if (!orders.length) return res.status(404).json({ error: 'Not found' });
  if (orders[0].user_id !== req.user.id && req.user.role !== 'admin') return res.status(403).json({ error: 'Forbidden' });
  const [items] = await pool.execute('SELECT * FROM order_items WHERE order_id=?', [req.params.id]);
  res.json({ ...orders[0], items });
});

app.post('/api/orders', auth, async (req, res) => {
  const { items, shipping_address, note } = req.body;
  const conn = await pool.getConnection();
  try {
    await conn.beginTransaction();
    let total = 0;
    for (const it of items) total += it.price * it.qty;
    const shipping = total > 750000 ? 0 : 35000;
    const final = total + shipping;
    const orderNum = genOrderNum();
    const [r] = await conn.execute('INSERT INTO orders (user_id, order_number, total_amount, shipping_cost, final_amount, shipping_address, note) VALUES (?,?,?,?,?,?,?)',
      [req.user.id, orderNum, total, shipping, final, shipping_address, note]);
    for (const it of items) {
      await conn.execute('INSERT INTO order_items (order_id, product_id, product_name, product_image, price, qty) VALUES (?,?,?,?,?,?)',
        [r.insertId, it.product_id, it.name, it.image, it.price, it.qty]);
    }
    await conn.execute('DELETE FROM cart_items WHERE user_id=?', [req.user.id]);
    await conn.commit();
    res.json({ order_id: r.insertId, order_number: orderNum, total: final });
  } catch (e) { await conn.rollback(); res.status(500).json({ error: e.message }); }
  finally { conn.release(); }
});

app.put('/api/orders/:id/status', auth, adminOnly, async (req, res) => {
  const { status } = req.body;
  await pool.execute('UPDATE orders SET status=? WHERE id=?', [status, req.params.id]);
  res.json({ updated: true });
});

// ========== REVIEWS ==========
app.get('/api/products/:id/reviews', async (req, res) => {
  const [rows] = await pool.execute(`SELECT r.*, u.name as user_name FROM reviews r JOIN users u ON r.user_id=u.id 
    WHERE r.product_id=? AND r.status="approved" ORDER BY r.created_at DESC`, [req.params.id]);
  res.json(rows);
});

app.post('/api/products/:id/reviews', auth, async (req, res) => {
  const { rating, comment } = req.body;
  await pool.execute('INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (?,?,?,?)', [req.user.id, req.params.id, rating, comment]);
  res.json({ submitted: true });
});

// ========== USERS (Admin) ==========
app.get('/api/users', auth, adminOnly, async (req, res) => {
  const [rows] = await pool.execute('SELECT id,name,email,phone,role,status,created_at FROM users');
  res.json(rows);
});

app.put('/api/users/:id', auth, adminOnly, async (req, res) => {
  const { status, role } = req.body;
  await pool.execute('UPDATE users SET status=COALESCE(?,status), role=COALESCE(?,role) WHERE id=?', [status, role, req.params.id]);
  res.json({ updated: true });
});

// ========== SETTINGS ==========
app.get('/api/settings', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM settings LIMIT 1');
  res.json(rows[0] || {});
});

app.put('/api/settings', auth, adminOnly, async (req, res) => {
  const fields = req.body;
  const sets = Object.keys(fields).map(k=>`${k}=?`).join(',');
  await pool.execute(`UPDATE settings SET ${sets} WHERE id=1`, Object.values(fields));
  res.json({ updated: true });
});

// ========== DASHBOARD STATS (Admin) ==========
app.get('/api/admin/stats', auth, adminOnly, async (req, res) => {
  const [[{ count: products }]] = await pool.execute('SELECT COUNT(*) as count FROM products WHERE status="active"');
  const [[{ count: orders }]] = await pool.execute('SELECT COUNT(*) as count FROM orders');
  const [[{ count: users }]] = await pool.execute('SELECT COUNT(*) as count FROM users');
  const [[{ revenue }]] = await pool.execute('SELECT COALESCE(SUM(final_amount),0) as revenue FROM orders WHERE payment_status="paid"');
  res.json({ products, orders, users, revenue });
});

// ========== BACKUP & RESTORE ==========
app.get('/api/admin/backup', auth, adminOnly, async (req, res) => {
  const [products] = await pool.execute('SELECT * FROM products');
  const [users] = await pool.execute('SELECT id,name,email,phone,role,status,created_at FROM users');
  const [orders] = await pool.execute('SELECT * FROM orders');
  const [articles] = await pool.execute('SELECT * FROM articles');
  res.json({ products, users, orders, articles, exported_at: new Date().toISOString() });
});



// ========== BANNERS ==========
app.get('/api/banners', async (req, res) => {
  const { position } = req.query;
  let sql = 'SELECT * FROM banners WHERE active=1';
  const params = [];
  if (position) { sql += ' AND position=?'; params.push(position); }
  sql += ' ORDER BY sort_order';
  const [rows] = await pool.execute(sql, params);
  res.json(rows);
});

app.post('/api/banners', auth, adminOnly, async (req, res) => {
  const { title, subtitle, image, link, position, sort_order } = req.body;
  const [r] = await pool.execute('INSERT INTO banners (title, subtitle, image, link, position, sort_order) VALUES (?,?,?,?,?,?)',
    [title, subtitle, image, link, position || 'main', sort_order || 0]);
  res.json({ id: r.insertId });
});

app.put('/api/banners/:id', auth, adminOnly, async (req, res) => {
  const { title, subtitle, image, link, position, sort_order, active } = req.body;
  await pool.execute('UPDATE banners SET title=COALESCE(?,title), subtitle=COALESCE(?,subtitle), image=COALESCE(?,image), link=COALESCE(?,link), position=COALESCE(?,position), sort_order=COALESCE(?,sort_order), active=COALESCE(?,active) WHERE id=?',
    [title, subtitle, image, link, position, sort_order, active, req.params.id]);
  res.json({ updated: true });
});

app.delete('/api/banners/:id', auth, adminOnly, async (req, res) => {
  await pool.execute('DELETE FROM banners WHERE id=?', [req.params.id]);
  res.json({ deleted: true });
});

// ========== MENUS ==========
app.get('/api/menus', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM menus WHERE active=1 ORDER BY sort_order');
  const parents = rows.filter(m => !m.parent_id);
  const result = parents.map(p => ({ ...p, submenu: rows.filter(c => c.parent_id === p.id) }));
  res.json(result);
});

app.post('/api/menus', auth, adminOnly, async (req, res) => {
  const { title, link, icon, parent_id, sort_order } = req.body;
  const [r] = await pool.execute('INSERT INTO menus (title, link, icon, parent_id, sort_order) VALUES (?,?,?,?,?)',
    [title, link, icon, parent_id || null, sort_order || 0]);
  res.json({ id: r.insertId });
});

app.put('/api/menus/:id', auth, adminOnly, async (req, res) => {
  const { title, link, icon, parent_id, sort_order, active } = req.body;
  await pool.execute('UPDATE menus SET title=COALESCE(?,title), link=COALESCE(?,link), icon=COALESCE(?,icon), parent_id=COALESCE(?,parent_id), sort_order=COALESCE(?,sort_order), active=COALESCE(?,active) WHERE id=?',
    [title, link, icon, parent_id, sort_order, active, req.params.id]);
  res.json({ updated: true });
});

app.delete('/api/menus/:id', auth, adminOnly, async (req, res) => {
  await pool.execute('DELETE FROM menus WHERE id=?', [req.params.id]);
  res.json({ deleted: true });
});

// ========== FOOTER LINKS ==========
app.get('/api/footer-links', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM footer_links WHERE active=1 ORDER BY sort_order');
  res.json(rows);
});

app.post('/api/footer-links', auth, adminOnly, async (req, res) => {
  const { title, link, sort_order } = req.body;
  const [r] = await pool.execute('INSERT INTO footer_links (title, link, sort_order) VALUES (?,?,?)', [title, link, sort_order || 0]);
  res.json({ id: r.insertId });
});

app.put('/api/footer-links/:id', auth, adminOnly, async (req, res) => {
  const { title, link, sort_order, active } = req.body;
  await pool.execute('UPDATE footer_links SET title=COALESCE(?,title), link=COALESCE(?,link), sort_order=COALESCE(?,sort_order), active=COALESCE(?,active) WHERE id=?',
    [title, link, sort_order, active, req.params.id]);
  res.json({ updated: true });
});

app.delete('/api/footer-links/:id', auth, adminOnly, async (req, res) => {
  await pool.execute('DELETE FROM footer_links WHERE id=?', [req.params.id]);
  res.json({ deleted: true });
});

// ========== PAGE TEXTS ==========
app.get('/api/page-texts', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM page_texts');
  const result = {};
  rows.forEach(r => { if (!result[r.section]) result[r.section] = {}; result[r.section][r.key_name] = r.value; });
  res.json(result);
});

app.get('/api/page-texts/:section', async (req, res) => {
  const [rows] = await pool.execute('SELECT * FROM page_texts WHERE section=?', [req.params.section]);
  const result = {};
  rows.forEach(r => result[r.key_name] = r.value);
  res.json(result);
});

app.put('/api/page-texts', auth, adminOnly, async (req, res) => {
  const { section, key_name, value } = req.body;
  await pool.execute('INSERT INTO page_texts (section, key_name, value) VALUES (?,?,?) ON DUPLICATE KEY UPDATE value=?',
    [section, key_name, value, value]);
  res.json({ updated: true });
});

// ========== ADMIN FULL DATA (for bridge) ==========
app.get('/api/admin/data', auth, adminOnly, async (req, res) => {
  const [products] = await pool.execute('SELECT p.*, b.nameFa as brandFa FROM products p LEFT JOIN brands b ON p.brand_id=b.id');
  const [orders] = await pool.execute('SELECT o.*, u.name as customer FROM orders o LEFT JOIN users u ON o.user_id=u.id ORDER BY o.created_at DESC');
  const [users] = await pool.execute('SELECT id,name,email,phone,status as active,created_at as date,avatar FROM users');
  const [banners] = await pool.execute('SELECT * FROM banners ORDER BY sort_order');
  const [menus] = await pool.execute('SELECT * FROM menus ORDER BY sort_order');
  const [footerLinks] = await pool.execute('SELECT * FROM footer_links ORDER BY sort_order');
  const [articles] = await pool.execute('SELECT id,title,excerpt,content,image,created_at as date FROM articles');
  const [pageTexts] = await pool.execute('SELECT * FROM page_texts');
  const [settingsRows] = await pool.execute('SELECT * FROM settings LIMIT 1');

  const texts = {};
  pageTexts.forEach(pt => { if (!texts[pt.section]) texts[pt.section] = {}; texts[pt.section][pt.key_name] = pt.value; });

  const settings = settingsRows[0] || {};

  res.json({ products, orders, users, banners, menus, footerLinks, articles: articles.map(a => ({...a, date: a.date ? new Date(a.date).toLocaleDateString('fa-IR') : ''})), texts, settings });
});

// ========== START ==========
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`DotWatch API running on http://localhost:${PORT}`));
