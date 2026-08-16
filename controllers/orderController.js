const { pool } = require('../config/database');
const { generateOrderNumber } = require('../utils/helpers');

exports.getOrders = async (req, res, next) => {
  try {
    let sql = `SELECT o.*, u.name as customer_name 
                 FROM orders o 
                 LEFT JOIN users u ON o.user_id = u.id 
                 WHERE 1=1`;
    const params = [];

    if (req.user.role !== 'admin' || req.query.all !== '1') {
      sql += ' AND o.user_id = ?';
      params.push(req.user.id);
    }
    sql += ' ORDER BY o.created_at DESC';

    const [rows] = await pool.execute(sql, params);
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

exports.getOrder = async (req, res, next) => {
  try {
    const [orders] = await pool.execute(
      'SELECT * FROM orders WHERE id = ?',
      [req.params.id]
    );
    if (!orders.length) return res.status(404).json({ error: 'Order not found' });

    const order = orders[0];
    if (order.user_id !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Forbidden' });
    }

    const [items] = await pool.execute(
      `SELECT oi.*, p.status as product_status, p.deleted_at 
       FROM order_items oi 
       LEFT JOIN products p ON oi.product_id = p.id 
       WHERE oi.order_id = ?`,
      [req.params.id]
    );
    res.json({ ...order, items });
  } catch (err) {
    next(err);
  }
};

exports.createOrder = async (req, res, next) => {
  const conn = await pool.getConnection();
  try {
    await conn.beginTransaction();
    const { items, shipping_address, note } = req.body;

    let total = 0;
    const orderItems = [];

    for (const it of items) {
      const [products] = await conn.execute(
        'SELECT id, name, image, price, stock, status, deleted_at FROM products WHERE id = ? FOR UPDATE',
        [it.product_id]
      );
      if (!products.length) {
        await conn.rollback();
        return res.status(404).json({ error: `Product ${it.product_id} not found` });
      }
      const product = products[0];
      if (product.status !== 'active' || product.deleted_at) {
        await conn.rollback();
        return res.status(400).json({ error: `Product ${product.name} is no longer available` });
      }
      if (product.stock < it.qty) {
        await conn.rollback();
        return res.status(400).json({ 
          error: `Insufficient stock for ${product.name}`, 
          available: product.stock,
          requested: it.qty 
        });
      }

      const itemTotal = product.price * it.qty;
      total += itemTotal;
      orderItems.push({
        product_id: product.id,
        name: product.name,
        image: product.image,
        price: product.price,
        qty: it.qty
      });

      await conn.execute(
        'UPDATE products SET stock = stock - ? WHERE id = ?',
        [it.qty, product.id]
      );
    }

    const [settings] = await conn.execute(
      'SELECT free_shipping_threshold FROM settings LIMIT 1'
    );
    const threshold = settings.length ? (settings[0].free_shipping_threshold || 750000) : 750000;
    const shipping = total >= threshold ? 0 : 35000;
    const final = total + shipping;

    const orderNum = generateOrderNumber();

    const [result] = await conn.execute(
      `INSERT INTO orders (user_id, order_number, total_amount, shipping_cost, final_amount, shipping_address, note) 
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
      [req.user.id, orderNum, total, shipping, final, shipping_address, note || null]
    );

    for (const it of orderItems) {
      await conn.execute(
        `INSERT INTO order_items (order_id, product_id, product_name, product_image, price, qty) 
         VALUES (?, ?, ?, ?, ?, ?)`,
        [result.insertId, it.product_id, it.name, it.image, it.price, it.qty]
      );
    }

    await conn.execute('DELETE FROM cart_items WHERE user_id = ?', [req.user.id]);

    await conn.commit();
    res.status(201).json({ order_id: result.insertId, order_number: orderNum, total: final });
  } catch (err) {
    await conn.rollback();
    next(err);
  } finally {
    conn.release();
  }
};

exports.updateOrderStatus = async (req, res, next) => {
  try {
    const { status } = req.body;
    const validStatuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ error: 'Invalid status' });
    }

    const [result] = await pool.execute(
      'UPDATE orders SET status = ? WHERE id = ?',
      [status, req.params.id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Order not found' });
    }
    res.json({ updated: true });
  } catch (err) {
    next(err);
  }
};
