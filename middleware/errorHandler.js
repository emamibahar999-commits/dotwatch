function errorHandler(err, req, res, next) {
  console.error(`[ERROR] ${req.method} ${req.path}:`, err);

  const isDev = process.env.NODE_ENV === 'development';

  if (err.code === 'ER_DUP_ENTRY') {
    return res.status(409).json({ error: 'Duplicate entry: Resource already exists' });
  }
  if (err.code === 'ER_NO_REFERENCED_ROW_2') {
    return res.status(400).json({ error: 'Invalid reference: Related resource not found' });
  }
  if (err.code === 'ER_BAD_FIELD_ERROR') {
    return res.status(400).json({ error: 'Invalid field name' });
  }

  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    ...(isDev && { stack: err.stack })
  });
}

module.exports = { errorHandler };
