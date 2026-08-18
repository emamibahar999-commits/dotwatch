const mysql = require('mysql2/promise');
require('dotenv').config();

async function testDB() {
  console.log('Testing database connection...\n');

  try {
    const pool = mysql.createPool({
      host: process.env.DB_HOST,
      user: process.env.DB_USER,
      password: process.env.DB_PASS,
      database: process.env.DB_NAME,
      waitForConnections: true,
      connectionLimit: 2,
    });

    const [rows] = await pool.execute('SELECT 1 as ok');
    console.log('✅ Database connection: OK');

    // Check tables
    const [tables] = await pool.execute(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = ?
    `, [process.env.DB_NAME]);

    console.log(`\n📋 Found ${tables.length} tables:`);
    tables.forEach(t => console.log(`   - ${t.TABLE_NAME || t.table_name}`));

    if (tables.length === 0) {
      console.log('\n⚠️  WARNING: No tables found! Run: mysql -u root -p < sql/dotwatch.sql');
    }

    await pool.end();
  } catch (err) {
    console.error('❌ Database connection failed:');
    console.error(`   ${err.message}\n`);
    console.log('💡 Make sure:');
    console.log('   1. MySQL is running');
    console.log('   2. .env file has correct DB_HOST, DB_USER, DB_PASS, DB_NAME');
    console.log('   3. Database exists: CREATE DATABASE dotwatch;');
  }
}

testDB();
