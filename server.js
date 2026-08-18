const express = require('express');
const helmet = require('helmet');
const morgan = require('morgan');
const cors = require('cors');
const compression = require('compression');
require('dotenv').config();

const { pool, closePool } = require('./config/database');
const { apiLimiter, authLimiter } = require('./middleware/rateLimiter');
const { errorHandler } = require('./middleware/errorHandler');

const app = express();

app.set('trust proxy', 1);
app.use(compression());

// CSP relaxed for inline styles/scripts used by static HTML files
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://code.jquery.com"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
      imgSrc: ["'self'", "https:", "data:", "blob:"],
      fontSrc: ["'self'", "https://cdn.jsdelivr.net", "https://fonts.gstatic.com"],
      connectSrc: ["'self'"],
    },
  },
  crossOriginEmbedderPolicy: false,
}));

app.use(morgan('combined'));

const allowedOrigins = (process.env.CORS_ORIGINS || 'http://localhost:3000').split(',');
app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.static('public'));

app.use('/api/auth', authLimiter);
app.use('/api', apiLimiter);

app.use('/api/auth', require('./routes/auth'));
app.use('/api/products', require('./routes/products'));
app.use('/api/cart', require('./routes/cart'));
app.use('/api/wishlist', require('./routes/wishlist'));
app.use('/api/orders', require('./routes/orders'));
app.use('/api', require('./routes/reviews'));
app.use('/api/articles', require('./routes/articles'));
app.use('/api/brands', require('./routes/brands'));
app.use('/api/accessories', require('./routes/accessories'));
app.use('/api/faqs', require('./routes/faqs'));
app.use('/api/banners', require('./routes/banners'));
app.use('/api/menus', require('./routes/menus'));
app.use('/api/footer-links', require('./routes/footerLinks'));
app.use('/api/page-texts', require('./routes/pageTexts'));
app.use('/api/settings', require('./routes/settings'));
app.use('/api/users', require('./routes/users'));
app.use('/api/admin', require('./routes/admin'));
app.use('/api/addresses', require('./routes/addresses'));
app.use('/api/payments', require('./routes/payments'));

app.get('/api/health', async (req, res) => {
  try {
    await pool.execute('SELECT 1 as ok');
    res.json({ status: 'ok', db: 'connected', timestamp: new Date().toISOString() });
  } catch (err) {
    res.status(500).json({ status: 'error', db: 'disconnected', error: err.message });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

app.use(errorHandler);

const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, () => {
  console.log(`DotWatch API running on http://localhost:${PORT}`);
});

process.on('SIGTERM', async () => {
  server.close(async () => { await closePool(); process.exit(0); });
});

process.on('SIGINT', async () => {
  server.close(async () => { await closePool(); process.exit(0); });
});