-- DotWatch Full Database Schema & Seed Data
-- MySQL 8.0+

CREATE DATABASE IF NOT EXISTS dotwatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dotwatch;

-- ==================== TABLES ====================

CREATE TABLE IF NOT EXISTS brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    name_fa VARCHAR(50) NOT NULL,
    logo VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    brand_id INT,
    price INT NOT NULL,
    old_price INT DEFAULT 0,
    discount TINYINT DEFAULT 0,
    gender ENUM('mens','ladies','unisex','couple') DEFAULT 'unisex',
    style ENUM('classic','casual','sport','luxury','minimal','smart') DEFAULT 'classic',
    type ENUM('quartz','automatic','digital','mechanical') DEFAULT 'quartz',
    material ENUM('steel','leather','mesh','resin','ceramic','silicone','rubber','fabric','two-tone') DEFAULT 'steel',
    color ENUM('silver','gold','rosegold','black','white','blue','brown','pink','red','green','two-tone','other') DEFAULT 'black',
    image VARCHAR(500),
    rating DECIMAL(2,1) DEFAULT 4.5,
    reviews INT DEFAULT 0,
    is_new TINYINT(1) DEFAULT 0,
    stock INT DEFAULT 0,
    movement VARCHAR(50),
    diameter VARCHAR(20),
    thickness VARCHAR(20),
    case_material VARCHAR(50),
    band_material VARCHAR(50),
    glass VARCHAR(50),
    water_resistant VARCHAR(50),
    weight VARCHAR(50),
    functions TEXT,
    features JSON,
    description TEXT,
    status ENUM('active','inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS accessories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    type ENUM('cufflinks','card-holder','strap','box','other') DEFAULT 'other',
    gender ENUM('mens','ladies','unisex') DEFAULT 'unisex',
    price INT NOT NULL,
    image VARCHAR(500),
    stock INT DEFAULT 0,
    status ENUM('active','inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    category VARCHAR(100),
    author VARCHAR(100) DEFAULT 'دات واچ',
    image VARCHAR(500),
    excerpt TEXT,
    content LONGTEXT,
    views INT DEFAULT 0,
    status ENUM('published','draft') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS faqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(500),
    role ENUM('user','admin') DEFAULT 'user',
    status ENUM('active','banned') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(50),
    city VARCHAR(50),
    address TEXT NOT NULL,
    postal_code VARCHAR(20),
    phone VARCHAR(20),
    is_default TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_number VARCHAR(20) UNIQUE,
    total_amount INT NOT NULL,
    shipping_cost INT DEFAULT 0,
    discount_amount INT DEFAULT 0,
    final_amount INT NOT NULL,
    status ENUM('pending','processing','shipped','delivered','cancelled') DEFAULT 'pending',
    payment_status ENUM('unpaid','paid','refunded') DEFAULT 'unpaid',
    shipping_address TEXT,
    tracking_code VARCHAR(50),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT,
    product_name VARCHAR(200),
    product_image VARCHAR(500),
    price INT NOT NULL,
    qty INT NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    qty INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_cart (user_id, product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS wishlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_wish (user_id, product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) DEFAULT 'دات واچ',
    store_email VARCHAR(100),
    store_phone VARCHAR(20),
    free_shipping_threshold INT DEFAULT 750000,
    maintenance_mode TINYINT(1) DEFAULT 0,
    allow_register TINYINT(1) DEFAULT 1,
    allow_reviews TINYINT(1) DEFAULT 1,
    primary_color VARCHAR(20) DEFAULT '#c9a96e',
    secondary_color VARCHAR(20) DEFAULT '#1a1a2e',
    bg_color VARCHAR(20) DEFAULT '#ffffff',
    text_color VARCHAR(20) DEFAULT '#333333',
    font_family VARCHAR(50) DEFAULT 'Vazirmatn',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==================== SEED DATA ====================

INSERT INTO brands (name, name_fa) VALUES
('Casio','کاسیو'),('Seiko','سیکو'),('Fossil','فسیل'),('Tissot','تیسوت'),
('Citizen','سیتیزن'),('G-Shock','جی شاک'),('DW','دنیل ولینگتون'),
('Romanson','رومانسون'),('Orient','اورینت'),('Apple','اپل'),
('Swarovski','سواروسکی'),('Invicta','اینویکتا'),('Angel','آنجل');

INSERT INTO products (id, name, brand_id, price, old_price, discount, gender, style, type, material, color, image, rating, reviews, is_new, stock, movement, diameter, thickness, case_material, band_material, glass, water_resistant, weight, functions, features) VALUES
(1,'ساعت مچی مردانه کاسیو ادیفایس EFV-550D',1,4850000,6200000,22,'mens','sport','quartz','steel','silver','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400',4.8,124,0,15,'کوارتز','45mm','12mm','استیل','استیل','معدنی','100 متر','160 گرم','کرونوگراف، تقویم','["chronograph","water-resistant"]'),
(2,'ساعت مچی زنانه فسیل جیانا ES4905',3,3200000,4500000,29,'ladies','classic','quartz','leather','brown','https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400',4.6,89,1,8,'کوارتز','36mm','8mm','استیل','چرم','معدنی','30 متر','45 گرم','تقویم','["calendar"]'),
(3,'ساعت مچی مردانه سیکو 5 اسپرت SRPD51',2,8900000,0,0,'mens','sport','automatic','steel','blue','https://images.unsplash.com/photo-1539874754764-5a96559165b0?w=400',4.9,210,0,5,'اتوماتیک','42.5mm','13.4mm','استیل','استیل','هاردلکس','100 متر','170 گرم','شبانه روز، تاریخ','["water-resistant"]'),
(4,'ساعت مچی زنانه دنیل ولینگتون پتیت',7,2100000,2800000,25,'ladies','minimal','quartz','mesh','rosegold','https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400',4.4,156,0,22,'کوارتز','28mm','6mm','استیل','مش','معدنی','30 متر','35 گرم','-','[]'),
(5,'ساعت ست رومانسون مدل 2026',8,5600000,7800000,28,'couple','luxury','quartz','steel','gold','https://images.unsplash.com/photo-1619134778706-7015533a6150?w=400',4.7,67,1,3,'کوارتز','38/32mm','9mm','استیل','استیل','سافایر','50 متر','120/90 گرم','تقویم','["calendar"]'),
(6,'ساعت مچی مردانه گشاک G-Steel GST-B100',6,12500000,0,0,'mens','sport','digital','resin','black','https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=400',4.9,340,0,12,'کوارتز/دیجیتال','55mm','14mm','رزین/استیل','رزین','معدنی','200 متر','120 گرم','بلوتوث، خورشیدی، کرونوگراف','["chronograph","water-resistant","calendar"]'),
(7,'ساعت مچی زنانه سواروسکی کریستالین',11,9800000,12000000,18,'ladies','luxury','quartz','ceramic','black','https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400',4.8,45,1,6,'کوارتز','35mm','8mm','استیل','سرامیک','سافایر','50 متر','80 گرم','تقویم','["calendar"]'),
(8,'ساعت مچی مردانه تیسوت پر 200',4,14200000,16800000,15,'mens','sport','quartz','steel','silver','https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400',4.7,98,0,7,'کوارتز','45mm','12mm','استیل','استیل','سافایر','200 متر','180 گرم','کرونوگراف، GMT، تقویم','["chronograph","water-resistant","gmt"]'),
(9,'ساعت مچی زنانه سیتیزن اکیو درایو EM0503',5,5600000,0,0,'ladies','classic','quartz','steel','silver','https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400',4.6,112,0,18,'اکیو-درایو','32mm','8mm','استیل','استیل','معدنی','50 متر','55 گرم','تقویم','["calendar"]'),
(10,'ساعت مچی مردانه اورینت مکانیکی Bambino',9,7200000,9500000,24,'mens','classic','automatic','leather','brown','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400',4.8,203,0,9,'اتوماتیک','42mm','12mm','استیل','چرم','معدنی','30 متر','65 گرم','-','[]'),
(11,'ساعت مچی زنانه آنجل سانشاین کریستال',13,1800000,2500000,28,'ladies','casual','quartz','silicone','pink','https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400',4.3,56,1,30,'کوارتز','38mm','10mm','آلیاژ','سیلیکون','معدنی','30 متر','40 گرم','-','[]'),
(12,'ساعت مچی مردانه اینویکتا پرو دیور 8926',12,3800000,0,0,'mens','sport','automatic','steel','two-tone','https://images.unsplash.com/photo-1539874754764-5a96559165b0?w=400',4.5,178,0,11,'اتوماتیک','40mm','14mm','استیل','استیل','فلورین','200 متر','155 گرم','تاریخ','["water-resistant"]'),
(13,'ساعت هوشمند اپل واچ سری 9 45mm',10,28000000,0,0,'unisex','smart','digital','silicone','black','https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400',4.9,520,1,20,'دیجیتال','45mm','10.7mm','آلومینیوم','سیلیکون','یاقوت کبود','50 متر','38 گرم','GPS، ضربان قلب، اکسیژن خون','["chronograph","water-resistant","calendar"]'),
(14,'ساعت مچی مردانه رومانسون اسکلتون',8,8900000,11000000,19,'mens','luxury','automatic','leather','black','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400',4.7,87,0,4,'اتوماتیک','42mm','12mm','استیل','چرم','معدنی','30 متر','70 گرم','نمایش مکانیزم','[]'),
(15,'ساعت مچی زنانه کاسیو شین SHE-4534',1,2600000,3200000,19,'ladies','minimal','quartz','steel','rosegold','https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400',4.5,134,0,16,'کوارتز','32mm','7mm','استیل','استیل','معدنی','50 متر','45 گرم','تقویم','["calendar"]'),
(16,'ساعت مچی مردانه سیکو پرساژ SSA231',2,10500000,0,0,'mens','classic','automatic','leather','brown','https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400',4.8,145,1,6,'اتوماتیک','40mm','12mm','استیل','چرم','هاردلکس','50 متر','60 گرم','تقویم، نمایش باز','["calendar"]'),
(17,'ساعت مچی زنانه تیسوت تی-کلاسیک',4,9800000,12000000,18,'ladies','classic','quartz','leather','black','https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400',4.6,92,0,10,'کوارتز','30mm','8mm','استیل','چرم','سافایر','30 متر','35 گرم','تقویم','["calendar"]'),
(18,'ساعت مچی مردانه فسیل نیت رایدر',3,4200000,5800000,28,'mens','casual','quartz','leather','brown','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400',4.5,167,0,14,'کوارتز','44mm','11mm','استیل','چرم','معدنی','50 متر','75 گرم','کرونوگراف، تقویم','["chronograph","calendar"]'),
(19,'ساعت مچی زنانه سیتیزن لطیفه EM0809',5,7200000,0,0,'ladies','luxury','quartz','ceramic','white','https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400',4.7,78,1,7,'اکیو-درایو','31mm','8mm','استیل','سرامیک','سافایر','50 متر','60 گرم','تقویم','["calendar"]'),
(20,'ساعت مچی مردانه گشاک GA-2100',6,6800000,8500000,20,'mens','sport','digital','resin','black','https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=400',4.8,289,0,25,'کوارتز/دیجیتال','48.5mm','11.8mm','کربن/رزین','رزین','معدنی','200 متر','51 گرم','کرونوگراف، تایمر، آلارم','["chronograph","water-resistant","calendar"]');

INSERT INTO accessories (id, name, type, gender, price, image, stock) VALUES
(101,'دکمه سردست لوکس مردانه نقره ای','cufflinks','mens',850000,'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400',20),
(102,'دکمه سردست طلایی کلاسیک','cufflinks','mens',1200000,'https://images.unsplash.com/photo-1620626012053-1a1c4f1a0e2a?w=400',15),
(103,'جاکارتی چرم طبیعی قهوه ای','card-holder','mens',450000,'https://images.unsplash.com/photo-1627123424574-181ce5171c98?w=400',30),
(104,'جاکارتی فلزی مینیمال','card-holder','unisex',320000,'https://images.unsplash.com/photo-1606503825008-909a6184f56d?w=400',45);

INSERT INTO articles (id, title, category, author, image, excerpt, content, status) VALUES
(1,'راهنمای جامع خرید ساعت مچی مردانه در 2026','راهنمای خرید','دات واچ','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600','در این مقاله به بررسی نکات مهم خرید ساعت مچی مردانه از جمله نوع موتور، سایز، متریال و برندهای معتبر می پردازیم...','<p>محتوای کامل مقاله...</p>','published'),
(2,'تاریخچه برند کاسیو: از ماشین حساب تا ساعت های جی شاک','تاریخچه برندها','دات واچ','https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=600','کاسیو یکی از بزرگترین تولیدکنندگان ساعت در جهان است...','<p>محتوای کامل مقاله...</p>','published'),
(3,'نحوه تشخیص ساعت اصل از فیک: راهنمای کامل','آموزش','دات واچ','https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600','با راهنمای جامع ما یاد بگیرید چگونه ساعت اصل را از تقلبی تشخیص دهید...','<p>محتوای کامل مقاله...</p>','published'),
(4,'مقایسه تکنولوژی Eco-Drive با ساعت های اتوماتیک','بررسی و مقایسه','دات واچ','https://images.unsplash.com/photo-1539874754764-5a96559165b0?w=600','تکنولوژی Eco-Drive سیتیزن در برابر موتورهای اتوماتیک سنتی...','<p>محتوای کامل مقاله...</p>','published'),
(5,'نگهداری و تعمیرات ساعت مکانیکی در منزل','نگهداری و تعمیرات','دات واچ','https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600','نکات کلیدی برای نگهداری صحیح از ساعت مکانیکی...','<p>محتوای کامل مقاله...</p>','published'),
(6,'بهترین ساعت های برند سیکو برای شروع کلکسیون','راهنمای خرید','دات واچ','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600','سیکو گزینه های عالی برای کلکسیونرهای تازه کار دارد...','<p>محتوای کامل مقاله...</p>','published');

INSERT INTO faqs (id, question, answer, sort_order) VALUES
(1,'چگونه از اصالت کالا مطمئن شوم؟','تمامی محصولات دات واچ همراه با کارت گارانتی شرکتی و هولوگرام اصالت عرضه می شوند. همچنین می توانید از طریق سایت رسمی برند، کد محصول را استعلام کنید.',1),
(2,'شرایط بازگشت کالا چیست؟','شما تا 7 روز پس از تحویل کالا فرصت دارید در صورت عدم استفاده و در شرایط اولیه، کالا را بازگشت دهید. هزینه ارسال بازگشت بر عهده مشتری است.',2),
(3,'آیا امکان خرید اقساطی وجود دارد؟','بله، برای خریدهای بالای 5 میلیون تومان می توانید از طریق درگاه های پارسیان و سامان، خرید اقساطی 12 ماهه داشته باشید.',3),
(4,'مدت زمان ارسال سفارش چقدر است؟','سفارش های تهران ظرف 24 ساعت کاری و سفارش شهرستان ها 2 تا 4 روز کاری تحویل داده می شوند.',4),
(5,'گارانتی محصولات شامل چه مواردی می شود؟','گارانتی شرکتی شامل موتور ساعت، شیشه و بند در برابر خرابی های غیرعمدی است. برای جزئیات بیشتر به صفحه شرایط گارانتی مراجعه کنید.',5);

INSERT INTO users (id, name, email, phone, password_hash, role, status) VALUES
(1,'مدیر سیستم','admin@dotwatch.ir','09120000000','$2b$10$adminhashplaceholder','admin','active');

INSERT INTO settings (id, store_name, store_email, store_phone, free_shipping_threshold) VALUES
(1,'دات واچ','info@dotwatch.ir','021-12345678',750000);




-- ===== ADDITIONAL TABLES FOR ADMIN PANEL =====

CREATE TABLE IF NOT EXISTS banners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    subtitle VARCHAR(300),
    image VARCHAR(500),
    link VARCHAR(500),
    position ENUM('main','promo','topbar') DEFAULT 'main',
    sort_order INT DEFAULT 0,
    active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    link VARCHAR(500),
    icon VARCHAR(50),
    parent_id INT DEFAULT NULL,
    sort_order INT DEFAULT 0,
    active TINYINT(1) DEFAULT 1,
    FOREIGN KEY (parent_id) REFERENCES menus(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS footer_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    link VARCHAR(500),
    sort_order INT DEFAULT 0,
    active TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS page_texts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section VARCHAR(50) NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    value TEXT,
    UNIQUE KEY unique_section_key (section, key_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===== ALTER PRODUCTS TO MATCH FRONTEND =====
ALTER TABLE products ADD COLUMN IF NOT EXISTS category VARCHAR(50) AFTER gender;
ALTER TABLE products ADD COLUMN IF NOT EXISTS description TEXT AFTER functions;
UPDATE products SET category = gender, description = COALESCE(description, name);

-- ===== SEED ADMIN DATA =====
INSERT INTO banners (id, title, subtitle, image, link, position, sort_order) VALUES
(1,'ساعت‌های زنانه لوکس','جدیدترین مدل‌های ساعت زنانه از برندهای معتبر','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=800','#','main',1),
(2,'ساعت‌های اسپرت مردانه','قدرت، دقت و مقاومت در کنار طراحی خیره‌کننده','https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=800','#','main',2),
(3,'ساعت‌های هوشمند روز','تکنولوژی آینده را امروز بر دستان خود احساس کنید','https://images.unsplash.com/photo-1546868871-af0c7a31de53?w=800','#','main',3),
(4,'ساعت مردانه','','https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400','#','promo',1),
(5,'ساعت زنانه','','https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400','#','promo',2),
(6,'ساعت ست','','https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?w=400','#','promo',3),
(7,'ساعت هوشمند','','https://images.unsplash.com/photo-1546868871-af0c7a31de53?w=400','#','promo',4);

INSERT INTO menus (id, title, link, icon, parent_id, sort_order) VALUES
(1,'صفحه اصلی','/','home',NULL,1),
(2,'ساعت مچی','#','clock',NULL,2),
(3,'مردانه','#',NULL,2,1),
(4,'زنانه','#',NULL,2,2),
(5,'ست','#',NULL,2,3),
(6,'اکسسوری','#','gem',NULL,3),
(7,'برندها','#','flag',NULL,4),
(8,'تماس','#','phone',NULL,5);

INSERT INTO footer_links (id, title, link, sort_order) VALUES
(1,'درباره ما','#',1),
(2,'قوانین','#',2),
(3,'سوالات متداول','#',3),
(4,'ارتباط با ما','#',4);

INSERT INTO page_texts (section, key_name, value) VALUES
('hero','title','جدیدترین مدل‌های ساعت'),
('hero','subtitle','مجموعه‌ای بی‌نظیر از برترین برندهای جهانی'),
('about','text','فروشگاه دات واچ از سال ۱۳۹۸ فعالیت خود را آغاز کرده و همواره در تلاش است تا بهترین ساعت‌های اورجینال را با مناسب‌ترین قیمت در اختیار مشتریان قرار دهد.'),
('features','json','[{"icon":"shield-alt","title":"ضمانت اصالت","desc":"۱۰۰٪ اورجینال با گارانتی"},{"icon":"truck","title":"ارسال رایگان","desc":"برای خرید بالای ۷۵۰ هزار"},{"icon":"undo","title":"۷ روز ضمانت","desc":"بازگشت بدون قید و شرط"},{"icon":"medal","title":"گارانتی شرکتی","desc":"معتبرترین گارانتی‌ها"}]'),
('sections','bestsellers','پرفروش‌ترین‌ها'),
('sections','offers','پیشنهاد امروز'),
('sections','discounts','تخفیف‌دارها'),
('sections','new','جدیدترین‌ها'),
('sections','brands','برندهای برتر'),
('sections','blog','آخرین مقالات');
