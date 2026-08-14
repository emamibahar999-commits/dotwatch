# DotWatch Backend

## نصب و راه‌اندازی سریع

### ۱. دیتابیس MySQL
```bash
mysql -u root -p < sql/dotwatch.sql
```

### ۲. نصب پکیج‌ها
```bash
npm install
```

### ۳. تنظیمات
فایل `.env` را ویرایش کنید و مشخصات دیتابیس خود را وارد کنید.

### ۴. اجرا
```bash
npm start
# یا برای توسعه:
npm run dev
```

## API Endpoints

### Auth
- `POST /api/auth/register` - ثبت‌نام
- `POST /api/auth/login` - ورود
- `GET /api/auth/me` - اطلاعات کاربر

### Products
- `GET /api/products?gender=mens&style=sport&sort=price-asc` - لیست محصولات
- `GET /api/products/:id` - جزئیات محصول
- `POST /api/products` - افزودن محصول (Admin)
- `PUT /api/products/:id` - ویرایش محصول (Admin)
- `DELETE /api/products/:id` - حذف محصول (Admin)

### Cart
- `GET /api/cart` - سبد خرید
- `POST /api/cart` - افزودن به سبد
- `PUT /api/cart/:product_id` - تغییر تعداد
- `DELETE /api/cart/:product_id` - حذف از سبد

### Wishlist
- `GET /api/wishlist` - لیست علاقه‌مندی‌ها
- `POST /api/wishlist` - افزودن/حذف

### Orders
- `GET /api/orders` - سفارشات
- `POST /api/orders` - ثبت سفارش
- `GET /api/orders/:id` - جزئیات سفارش

### Articles, FAQs, Brands, Settings, Reviews

### Admin
- `GET /api/admin/stats` - آمار داشبورد
- `GET /api/admin/backup` - خروجی JSON
- `GET /api/users` - لیست کاربران

## توکن ادمین پیش‌فرض
ایمیل: `admin@dotwatch.ir`  
برای ست کردن پسورد مستقیم در دیتابیس از bcrypt استفاده کنید.
