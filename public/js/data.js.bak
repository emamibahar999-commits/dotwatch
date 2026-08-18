
const DB = {
  products: [
    { id: 1, name: "ساعت مچی مردانه کاسیو ادیفایس EFV-550D", brand: "Casio", brandFa: "کاسیو", price: 4850000, oldPrice: 6200000, discount: 22, gender: "mens", style: "sport", type: "quartz", feature: ["chronograph","water-resistant"], material: "steel", color: "silver", image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400", rating: 4.8, reviews: 124, isNew: false, stock: 15, specs: {movement:"کوارتز", diameter:"45mm", thickness:"12mm", case:"استیل", band:"استیل", glass:"معدنی", water:"100 متر", weight:"160 گرم", functions:"کرونوگراف، تقویم"} },
    { id: 2, name: "ساعت مچی زنانه فسیل جیانا ES4905", brand: "Fossil", brandFa: "فسیل", price: 3200000, oldPrice: 4500000, discount: 29, gender: "ladies", style: "classic", type: "quartz", feature: ["calendar"], material: "leather", color: "brown", image: "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400", rating: 4.6, reviews: 89, isNew: true, stock: 8, specs: {movement:"کوارتز", diameter:"36mm", thickness:"8mm", case:"استیل", band:"چرم", glass:"معدنی", water:"30 متر", weight:"45 گرم", functions:"تقویم"} },
    { id: 3, name: "ساعت مچی مردانه سیکو 5 اسپرت SRPD51", brand: "Seiko", brandFa: "سیکو", price: 8900000, oldPrice: 0, discount: 0, gender: "mens", style: "sport", type: "automatic", feature: ["water-resistant"], material: "steel", color: "blue", image: "https://images.unsplash.com/photo-1539874754764-5a96559165b0?w=400", rating: 4.9, reviews: 210, isNew: false, stock: 5, specs: {movement:"اتوماتیک", diameter:"42.5mm", thickness:"13.4mm", case:"استیل", band:"استیل", glass:"هاردلکس", water:"100 متر", weight:"170 گرم", functions:"شبانه روز، تاریخ"} },
    { id: 4, name: "ساعت مچی زنانه دنیل ولینگتون پتیت", brand: "DW", brandFa: "دنیل ولینگتون", price: 2100000, oldPrice: 2800000, discount: 25, gender: "ladies", style: "minimal", type: "quartz", feature: [], material: "mesh", color: "rosegold", image: "https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400", rating: 4.4, reviews: 156, isNew: false, stock: 22, specs: {movement:"کوارتز", diameter:"28mm", thickness:"6mm", case:"استیل", band:"مش", glass:"معدنی", water:"30 متر", weight:"35 گرم", functions:"-"} },
    { id: 5, name: "ساعت ست رومانسون مدل 2026", brand: "Romanson", brandFa: "رومانسون", price: 5600000, oldPrice: 7800000, discount: 28, gender: "couple", style: "luxury", type: "quartz", feature: ["calendar"], material: "steel", color: "gold", image: "https://images.unsplash.com/photo-1619134778706-7015533a6150?w=400", rating: 4.7, reviews: 67, isNew: true, stock: 3, specs: {movement:"کوارتز", diameter:"38/32mm", thickness:"9mm", case:"استیل", band:"استیل", glass:"سافایر", water:"50 متر", weight:"120/90 گرم", functions:"تقویم"} },
    { id: 6, name: "ساعت مچی مردانه گشاک G-Steel GST-B100", brand: "G-Shock", brandFa: "جی شاک", price: 12500000, oldPrice: 0, discount: 0, gender: "mens", style: "sport", type: "digital", feature: ["chronograph","water-resistant","calendar"], material: "resin", color: "black", image: "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=400", rating: 4.9, reviews: 340, isNew: false, stock: 12, specs: {movement:"کوارتز/دیجیتال", diameter:"55mm", thickness:"14mm", case:"رزین/استیل", band:"رزین", glass:"معدنی", water:"200 متر", weight:"120 گرم", functions:"بلوتوث، خورشیدی، کرونوگراف"} },
    { id: 7, name: "ساعت مچی زنانه سواروسکی کریستالین", brand: "Swarovski", brandFa: "سواروسکی", price: 9800000, oldPrice: 12000000, discount: 18, gender: "ladies", style: "luxury", type: "quartz", feature: ["calendar"], material: "ceramic", color: "black", image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400", rating: 4.8, reviews: 45, isNew: true, stock: 6, specs: {movement:"کوارتز", diameter:"35mm", thickness:"8mm", case:"استیل", band:"سرامیک", glass:"سافایر", water:"50 متر", weight:"80 گرم", functions:"تقویم"} },
    { id: 8, name: "ساعت مچی مردانه تیسوت پر 200", brand: "Tissot", brandFa: "تیسوت", price: 14200000, oldPrice: 16800000, discount: 15, gender: "mens", style: "sport", type: "quartz", feature: ["chronograph","water-resistant","gmt"], material: "steel", color: "silver", image: "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400", rating: 4.7, reviews: 98, isNew: false, stock: 7, specs: {movement:"کوارتز", diameter:"45mm", thickness:"12mm", case:"استیل", band:"استیل", glass:"سافایر", water:"200 متر", weight:"180 گرم", functions:"کرونوگراف، GMT، تقویم"} },
    { id: 9, name: "ساعت مچی زنانه سیتیزن اکیو درایو EM0503", brand: "Citizen", brandFa: "سیتیزن", price: 5600000, oldPrice: 0, discount: 0, gender: "ladies", style: "classic", type: "quartz", feature: ["calendar"], material: "steel", color: "silver", image: "https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400", rating: 4.6, reviews: 112, isNew: false, stock: 18, specs: {movement:"اکیو-درایو", diameter:"32mm", thickness:"8mm", case:"استیل", band:"استیل", glass:"معدنی", water:"50 متر", weight:"55 گرم", functions:"تقویم"} },
    { id: 10, name: "ساعت مچی مردانه اورینت مکانیکی Bambino", brand: "Orient", brandFa: "اورینت", price: 7200000, oldPrice: 9500000, discount: 24, gender: "mens", style: "classic", type: "automatic", feature: [], material: "leather", color: "brown", image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400", rating: 4.8, reviews: 203, isNew: false, stock: 9, specs: {movement:"اتوماتیک", diameter:"42mm", thickness:"12mm", case:"استیل", band:"چرم", glass:"معدنی", water:"30 متر", weight:"65 گرم", functions:"-"} },
    { id: 11, name: "ساعت مچی زنانه آنجل سانشاین کریستال", brand: "Angel", brandFa: "آنجل", price: 1800000, oldPrice: 2500000, discount: 28, gender: "ladies", style: "casual", type: "quartz", feature: [], material: "silicone", color: "pink", image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400", rating: 4.3, reviews: 56, isNew: true, stock: 30, specs: {movement:"کوارتز", diameter:"38mm", thickness:"10mm", case:"آلیاژ", band:"سیلیکون", glass:"معدنی", water:"30 متر", weight:"40 گرم", functions:"-"} },
    { id: 12, name: "ساعت مچی مردانه اینویکتا پرو دیور 8926", brand: "Invicta", brandFa: "اینویکتا", price: 3800000, oldPrice: 0, discount: 0, gender: "mens", style: "sport", type: "automatic", feature: ["water-resistant"], material: "steel", color: "two-tone", image: "https://images.unsplash.com/photo-1539874754764-5a96559165b0?w=400", rating: 4.5, reviews: 178, isNew: false, stock: 11, specs: {movement:"اتوماتیک", diameter:"40mm", thickness:"14mm", case:"استیل", band:"استیل", glass:"فلورین", water:"200 متر", weight:"155 گرم", functions:"تاریخ"} },
    { id: 13, name: "ساعت هوشمند اپل واچ سری 9 45mm", brand: "Apple", brandFa: "اپل", price: 28000000, oldPrice: 0, discount: 0, gender: "unisex", style: "smart", type: "digital", feature: ["chronograph","water-resistant","calendar"], material: "silicone", color: "black", image: "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400", rating: 4.9, reviews: 520, isNew: true, stock: 20, specs: {movement:"دیجیتال", diameter:"45mm", thickness:"10.7mm", case:"آلومینیوم", band:"سیلیکون", glass:"یاقوت کبود", water:"50 متر", weight:"38 گرم", functions:"GPS، ضربان قلب، اکسیژن خون"} },
    { id: 14, name: "ساعت مچی مردانه رومانسون اسکلتون", brand: "Romanson", brandFa: "رومانسون", price: 8900000, oldPrice: 11000000, discount: 19, gender: "mens", style: "luxury", type: "automatic", feature: [], material: "leather", color: "black", image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400", rating: 4.7, reviews: 87, isNew: false, stock: 4, specs: {movement:"اتوماتیک", diameter:"42mm", thickness:"12mm", case:"استیل", band:"چرم", glass:"معدنی", water:"30 متر", weight:"70 گرم", functions:"نمایش مکانیزم"} },
    { id: 15, name: "ساعت مچی زنانه کاسیو شین SHE-4534", brand: "Casio", brandFa: "کاسیو", price: 2600000, oldPrice: 3200000, discount: 19, gender: "ladies", style: "minimal", type: "quartz", feature: ["calendar"], material: "steel", color: "rosegold", image: "https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400", rating: 4.5, reviews: 134, isNew: false, stock: 16, specs: {movement:"کوارتز", diameter:"32mm", thickness:"7mm", case:"استیل", band:"استیل", glass:"معدنی", water:"50 متر", weight:"45 گرم", functions:"تقویم"} },
    { id: 16, name: "ساعت مچی مردانه سیکو پرساژ SSA231", brand: "Seiko", brandFa: "سیکو", price: 10500000, oldPrice: 0, discount: 0, gender: "mens", style: "classic", type: "automatic", feature: ["calendar"], material: "leather", color: "brown", image: "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400", rating: 4.8, reviews: 145, isNew: true, stock: 6, specs: {movement:"اتوماتیک", diameter:"40mm", thickness:"12mm", case:"استیل", band:"چرم", glass:"هاردلکس", water:"50 متر", weight:"60 گرم", functions:"تقویم، نمایش باز"} },
    { id: 17, name: "ساعت مچی زنانه تیسوت تی-کلاسیک", brand: "Tissot", brandFa: "تیسوت", price: 9800000, oldPrice: 12000000, discount: 18, gender: "ladies", style: "classic", type: "quartz", feature: ["calendar"], material: "leather", color: "black", image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400", rating: 4.6, reviews: 92, isNew: false, stock: 10, specs: {movement:"کوارتز", diameter:"30mm", thickness:"8mm", case:"استیل", band:"چرم", glass:"سافایر", water:"30 متر", weight:"35 گرم", functions:"تقویم"} },
    { id: 18, name: "ساعت مچی مردانه فسیل نیت رایدر", brand: "Fossil", brandFa: "فسیل", price: 4200000, oldPrice: 5800000, discount: 28, gender: "mens", style: "casual", type: "quartz", feature: ["chronograph","calendar"], material: "leather", color: "brown", image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400", rating: 4.5, reviews: 167, isNew: false, stock: 14, specs: {movement:"کوارتز", diameter:"44mm", thickness:"11mm", case:"استیل", band:"چرم", glass:"معدنی", water:"50 متر", weight:"75 گرم", functions:"کرونوگراف، تقویم"} },
    { id: 19, name: "ساعت مچی زنانه سیتیزن لطیفه EM0809", brand: "Citizen", brandFa: "سیتیزن", price: 7200000, oldPrice: 0, discount: 0, gender: "ladies", style: "luxury", type: "quartz", feature: ["calendar"], material: "ceramic", color: "white", image: "https://images.unsplash.com/photo-1434056886845-dbe89f8f5d0e?w=400", rating: 4.7, reviews: 78, isNew: true, stock: 7, specs: {movement:"اکیو-درایو", diameter:"31mm", thickness:"8mm", case:"استیل", band:"سرامیک", glass:"سافایر", water:"50 متر", weight:"60 گرم", functions:"تقویم"} },
    { id: 20, name: "ساعت مچی مردانه گشاک GA-2100", brand: "G-Shock", brandFa: "جی شاک", price: 6800000, oldPrice: 8500000, discount: 20, gender: "mens", style: "sport", type: "digital", feature: ["chronograph","water-resistant","calendar"], material: "resin", color: "black", image: "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=400", rating: 4.8, reviews: 289, isNew: false, stock: 25, specs: {movement:"کوارتز/دیجیتال", diameter:"48.5mm", thickness:"11.8mm", case:"کربن/رزین", band:"رزین", glass:"معدنی", water:"200 متر", weight:"51 گرم", functions:"کرونوگراف، تایمر، آلارم"} }
  ],

  accessories: [
    { id: 101, name: "دکمه سردست لوکس مردانه نقره ای", type: "cufflinks", gender: "mens", price: 850000, image: "https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400", stock: 20 },
    { id: 102, name: "دکمه سردست طلایی کلاسیک", type: "cufflinks", gender: "mens", price: 1200000, image: "https://images.unsplash.com/photo-1620626012053-1a1c4f1a0e2a?w=400", stock: 15 },
    { id: 103, name: "جاکارتی چرم طبیعی قهوه ای", type: "card-holder", gender: "mens", price: 450000, image: "https://images.unsplash.com/photo-1627123424574-181ce5171c98?w=400", stock: 30 },
    { id: 104, name: "جاکارتی فلزی مینیمال", type: "card-holder", gender: "unisex", price: 320000, image: "https://images.unsplash.com/photo-1606503825008-909a6184f56d?w=400", stock: 45 }
  ],

  articles: [
    { id: 1, title: "راهنمای جامع خرید ساعت مچی مردانه در 2026", category: "راهنمای خرید", date: "15 مرداد 1405", author: "دات واچ", image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600", excerpt: "در این مقاله به بررسی نکات مهم خرید ساعت مچی مردانه از جمله نوع موتور، سایز، متریال و برندهای معتبر می پردازیم..." },
    { id: 2, title: "تاریخچه برند کاسیو: از ماشین حساب تا ساعت های جی شاک", category: "تاریخچه برندها", date: "10 مرداد 1405", author: "دات واچ", image: "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=600", excerpt: "کاسیو یکی از بزرگترین تولیدکنندگان ساعت در جهان است. در این مقاله تاریخچه این برند ژاپنی را از تاسیس تا به امروز بررسی می کنیم..." },
    { id: 3, title: "نحوه تشخیص ساعت اصل از فیک: راهنمای کامل", category: "آموزش", date: "5 مرداد 1405", author: "دات واچ", image: "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600", excerpt: "با راهنمای جامع ما یاد بگیرید چگونه ساعت اصل را از تقلبی تشخیص دهید و از خرید خود مطمئن شوید..." },
    { id: 4, title: "مقایسه تکنولوژی Eco-Drive با ساعت های اتوماتیک", category: "بررسی و مقایسه", date: "1 مرداد 1405", author: "دات واچ", image: "https://images.unsplash.com/photo-1539874754764-5a96559165b0?w=600", excerpt: "تکنولوژی Eco-Drive سیتیزن در برابر موتورهای اتوماتیک سنتی: کدام یک برای شما مناسب تر است؟" },
    { id: 5, title: "نگهداری و تعمیرات ساعت مکانیکی در منزل", category: "نگهداری و تعمیرات", date: "25 تیر 1405", author: "دات واچ", image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600", excerpt: "نکات کلیدی برای نگهداری صحیح از ساعت مکانیکی و افزایش عمر آن..." },
    { id: 6, title: "بهترین ساعت های برند سیکو برای شروع کلکسیون", category: "راهنمای خرید", date: "20 تیر 1405", author: "دات واچ", image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600", excerpt: "سیکو گزینه های عالی برای کلکسیونرهای تازه کار دارد. در این مقاله 5 مدل برتر را معرفی می کنیم..." }
  ],

  brands: [
    { name: "Casio", nameFa: "کاسیو" },
    { name: "Seiko", nameFa: "سیکو" },
    { name: "Fossil", nameFa: "فسیل" },
    { name: "Tissot", nameFa: "تیسوت" },
    { name: "Citizen", nameFa: "سیتیزن" },
    { name: "G-Shock", nameFa: "جی شاک" },
    { name: "DW", nameFa: "دنیل ولینگتون" },
    { name: "Romanson", nameFa: "رومانسون" },
    { name: "Orient", nameFa: "اورینت" },
    { name: "Apple", nameFa: "اپل" }
  ],

  faqs: [
    { q: "چگونه از اصالت کالا مطمئن شوم؟", a: "تمامی محصولات دات واچ همراه با کارت گارانتی شرکتی و هولوگرام اصالت عرضه می شوند. همچنین می توانید از طریق سایت رسمی برند، کد محصول را استعلام کنید." },
    { q: "شرایط بازگشت کالا چیست؟", a: "شما تا 7 روز پس از تحویل کالا فرصت دارید در صورت عدم استفاده و در شرایط اولیه، کالا را بازگشت دهید. هزینه ارسال بازگشت بر عهده مشتری است." },
    { q: "آیا امکان خرید اقساطی وجود دارد؟", a: "بله، برای خریدهای بالای 5 میلیون تومان می توانید از طریق درگاه های پارسیان و سامان، خرید اقساطی 12 ماهه داشته باشید." },
    { q: "مدت زمان ارسال سفارش چقدر است؟", a: "سفارش های تهران ظرف 24 ساعت کاری و سفارش شهرستان ها 2 تا 4 روز کاری تحویل داده می شوند." },
    { q: "گارانتی محصولات شامل چه مواردی می شود؟", a: "گارانتی شرکتی شامل موتور ساعت، شیشه و بند در برابر خرابی های غیرعمدی است. برای جزئیات بیشتر به صفحه شرایط گارانتی مراجعه کنید." }
  ]
};

const Store = {
  cart: JSON.parse(localStorage.getItem('dotwatch_v2_cart') || '[]'),
  wishlist: JSON.parse(localStorage.getItem('dotwatch_v2_wishlist') || '[]'),
  compare: JSON.parse(localStorage.getItem('dotwatch_v2_compare') || '[]'),
  viewed: JSON.parse(localStorage.getItem('dotwatch_v2_viewed') || '[]'),

  save() {
    localStorage.setItem('dotwatch_v2_cart', JSON.stringify(this.cart));
    localStorage.setItem('dotwatch_v2_wishlist', JSON.stringify(this.wishlist));
    localStorage.setItem('dotwatch_v2_compare', JSON.stringify(this.compare));
    localStorage.setItem('dotwatch_v2_viewed', JSON.stringify(this.viewed));
    this.updateBadges();
  },

  addToCart(product, qty = 1) {
    const existing = this.cart.find(item => item.id === product.id);
    if (existing) existing.qty += qty;
    else this.cart.push({ ...product, qty });
    this.save();
    showNotification(product.name + ' به سبد خرید اضافه شد');
  },

  removeFromCart(id) {
    this.cart = this.cart.filter(item => item.id !== id);
    this.save();
    renderCart();
  },

  toggleWishlist(product) {
    const idx = this.wishlist.findIndex(item => item.id === product.id);
    if (idx >= 0) {
      this.wishlist.splice(idx, 1);
      showNotification('از علاقه مندی ها حذف شد');
    } else {
      this.wishlist.push(product);
      showNotification('به علاقه مندی ها اضافه شد');
    }
    this.save();
    renderWishlist();
  },

  toggleCompare(product) {
    const idx = this.compare.findIndex(item => item.id === product.id);
    if (idx >= 0) {
      this.compare.splice(idx, 1);
      showNotification('از مقایسه حذف شد');
    } else {
      if (this.compare.length >= 4) {
        showNotification('حداکثر 4 محصول می توانید مقایسه کنید');
        return;
      }
      this.compare.push(product);
      showNotification('به مقایسه اضافه شد');
    }
    this.save();
    renderCompare();
  },

  addViewed(product) {
    this.viewed = this.viewed.filter(p => p.id !== product.id);
    this.viewed.unshift(product);
    if (this.viewed.length > 10) this.viewed.pop();
    this.save();
  },

  updateBadges() {
    const cartBadge = document.getElementById('cart-count');
    const wishBadge = document.getElementById('wish-count');
    const compareBadge = document.getElementById('compare-count');
    if (cartBadge) cartBadge.textContent = this.cart.reduce((a,b)=>a+b.qty,0);
    if (wishBadge) wishBadge.textContent = this.wishlist.length;
    if (compareBadge) compareBadge.textContent = this.compare.length;
  },

  getCartTotal() {
    return this.cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  }
};

function showNotification(msg) {
  const bar = document.getElementById('notification-bar');
  if (!bar) return;
  bar.querySelector('span').textContent = msg;
  bar.classList.add('show');
  setTimeout(() => bar.classList.remove('show'), 3000);
}

function formatPrice(price) {
  return price.toLocaleString('fa-IR') + ' تومان';
}

function getProductUrl(id) {
  return '../watch/detail.html?id=' + id;
}

document.addEventListener('DOMContentLoaded', () => Store.updateBadges());
