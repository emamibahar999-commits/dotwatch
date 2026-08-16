# DotWatch Backend - Fixed & Secure

## تغییرات اصلی

### امنیت
- رفع SQL Injection با whitelist کردن نام ستون‌ها
- JWT Secret اجباری در `.env`
- Rate Limiting روی Auth و API
- Helmet برای Security Headers
- CORS محدود به دامنه‌های مجاز
- Validation کامل ورودی‌ها با express-validator
- بررسی موجودی انبار در سبد خرید و ثبت سفارش
- قیمت‌گذاری از دیتابیس (نه کلاینت)

### معماری
- جداسازی به MVC (Routes, Controllers, Models)
- Global Error Handler
- Graceful Shutdown
- Morgan Logger

### دیتابیس
- Index‌های بهینه روی همه جداول
- Soft Delete (`deleted_at`)
- API آدرس‌ها (`/api/addresses`)

## نصب

```bash
# 1. دیتابیس
mysql -u root -p < sql/dotwatch.sql

# 2. env
cp .env.example .env
# ویرایش .env

# 3. پکیج‌ها
npm install

# 4. اجرا
npm run dev
```

## پسورد ادمین پیش‌فرض
- ایمیل: `admin@dotwatch.ir`
- پسورد: `Admin@1234`
