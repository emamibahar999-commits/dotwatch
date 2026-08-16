const { pool } = require('../config/database');

exports.getStats = async (req, res, next) => {
  try {
    const [[{ count: products }]] = await pool.execute(
      'SELECT COUNT(*) as count FROM products WHERE status = "active" AND deleted_at IS NULL'
    );
    const [[{ count: orders }]] = await pool.execute(
      'SELECT COUNT(*) as count FROM orders'
    );
    const [[{ count: users }]] = await pool.execute(
      'SELECT COUNT(*) as count FROM users WHERE deleted_at IS NULL'
    );
    const [[{ revenue }]] = await pool.execute(
      'SELECT COALESCE(SUM(final_amount), 0) as revenue FROM orders WHERE payment_status = "paid"'
    );
    res.json({ products, orders, users, revenue });
  } catch (err) {
    next(err);
  }
};

exports.getBackup = async (req, res, next) => {
  try {
    const [products] = await pool.execute(
      'SELECT id, name, brand_id, price, stock, status, created_at FROM products WHERE deleted_at IS NULL'
    );
    const [users] = await pool.execute(
      'SELECT id, name, email, phone, role, status, created_at FROM users WHERE deleted_at IS NULL'
    );
    const [orders] = await pool.execute(
      'SELECT id, order_number, user_id, total_amount, final_amount, status, payment_status, created_at FROM orders'
    );
    const [articles] = await pool.execute(
      'SELECT id, title, category, author, status, created_at FROM articles WHERE deleted_at IS NULL'
    );
    res.json({ products, users, orders, articles, exported_at: new Date().toISOString() });
  } catch (err) {
    next(err);
  }
};

exports.getFullData = async (req, res, next) => {
  try {
    const [products] = await pool.execute(
      `SELECT p.*, b.nameFa as brandFa FROM products p 
       LEFT JOIN brands b ON p.brand_id = b.id WHERE p.deleted_at IS NULL`
    );
    const [orders] = await pool.execute(
      `SELECT o.*, u.name as customer FROM orders o 
       LEFT JOIN users u ON o.user_id = u.id ORDER BY o.created_at DESC`
    );
    const [users] = await pool.execute(
      'SELECT id, name, email, phone, status as active, created_at as date, avatar FROM users WHERE deleted_at IS NULL'
    );
    const [banners] = await pool.execute('SELECT * FROM banners ORDER BY sort_order');
    const [menus] = await pool.execute('SELECT * FROM menus ORDER BY sort_order');
    const [footerLinks] = await pool.execute('SELECT * FROM footer_links ORDER BY sort_order');
    const [articles] = await pool.execute(
      'SELECT id, title, excerpt, content, image, created_at as date FROM articles WHERE deleted_at IS NULL'
    );
    const [pageTexts] = await pool.execute('SELECT * FROM page_texts');
    const [settingsRows] = await pool.execute('SELECT * FROM settings LIMIT 1');

    const texts = {};
    pageTexts.forEach(pt => {
      if (!texts[pt.section]) texts[pt.section] = {};
      texts[pt.section][pt.key_name] = pt.value;
    });

    res.json({
      products, orders, users, banners, menus, footerLinks,
      articles: articles.map(a => ({
        ...a,
        date: a.date ? new Date(a.date).toLocaleDateString('fa-IR') : ''
      })),
      texts,
      settings: settingsRows[0] || {}
    });
  } catch (err) {
    next(err);
  }
};
