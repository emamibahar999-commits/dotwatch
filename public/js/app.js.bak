
// ==================== DOTWATCH APP ====================

function renderProductCard(p) {
  return `
    <div class="product-card fade-in">
      <div class="product-img">
        <img src="${p.image}" alt="${p.name}" loading="lazy">
        <div class="product-actions">
          <button class="action-icon" onclick="Store.toggleWishlist(DB.products.find(x=>x.id===${p.id}));event.stopPropagation();" title="علاقه‌مندی">♥</button>
          <button class="action-icon" onclick="Store.toggleCompare(DB.products.find(x=>x.id===${p.id}));event.stopPropagation();" title="مقایسه">⇄</button>
          <button class="action-icon" onclick="Store.addToCart(DB.products.find(x=>x.id===${p.id}));event.stopPropagation();" title="سبد خرید">🛒</button>
        </div>
      </div>
      <div class="product-info">
        <div class="product-brand">${p.brandFa}</div>
        <h3 class="product-title"><a href="${getProductUrl(p.id)}">${p.name}</a></h3>
        <div class="product-price">
          <span class="price-current">${formatPrice(p.price)}</span>
        </div>
      </div>
    </div>
  `;
}

function renderProducts(containerId, products) {
  const container = document.getElementById(containerId);
  if (!container) return;
  if (products.length === 0) {
    container.innerHTML = `<div class="empty-state"><h3>محصولی یافت نشد</h3><p>با فیلترهای دیگری امتحان کنید</p></div>`;
    return;
  }
  container.innerHTML = products.map(renderProductCard).join('');
}

function renderBlogCard(a) {
  return `
    <div class="blog-card fade-in">
      <div class="blog-img"><img src="${a.image}" alt="${a.title}" loading="lazy"></div>
      <div class="blog-content">
        <div class="blog-meta"><span>📅 ${a.date}</span><span>✍️ ${a.author}</span><span>📁 ${a.category}</span></div>
        <h3><a href="detail.html?id=${a.id}">${a.title}</a></h3>
        <p>${a.excerpt}</p>
        <a href="detail.html?id=${a.id}" class="btn-outline" style="margin-top:15px">ادامه مطلب →</a>
      </div>
    </div>
  `;
}

function setupFilters() {
  const checkboxes = document.querySelectorAll('.filter-option input[type="checkbox"]');
  checkboxes.forEach(cb => {
    cb.addEventListener('change', applyFilters);
  });

  const priceInputs = document.querySelectorAll('.price-range input');
  priceInputs.forEach(inp => {
    inp.addEventListener('input', debounce(applyFilters, 300));
  });

  const sortSelect = document.getElementById('sort-select');
  if (sortSelect) sortSelect.addEventListener('change', applyFilters);
}

function debounce(fn, ms) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

function applyFilters() {
  let products = [...DB.products];

  // Category filter from page config
  if (window.PAGE_CONFIG && window.PAGE_CONFIG.filter) {
    const cfg = window.PAGE_CONFIG;
    if (cfg.filterType === 'gender') products = products.filter(p => p.gender === cfg.filter || (cfg.filter === 'mens' && p.gender === 'unisex'));
    else if (cfg.filterType === 'style') products = products.filter(p => p.style === cfg.filter);
    else if (cfg.filterType === 'type') products = products.filter(p => p.type === cfg.filter);
    else if (cfg.filterType === 'feature') products = products.filter(p => p.feature.includes(cfg.filter));
    else if (cfg.filterType === 'material') products = products.filter(p => p.material === cfg.filter);
    else if (cfg.filterType === 'color') products = products.filter(p => p.color === cfg.filter);
  }

  // Sidebar filters
  const checkedBrands = Array.from(document.querySelectorAll('[data-filter="brand"]:checked')).map(cb => cb.value);
  if (checkedBrands.length) products = products.filter(p => checkedBrands.includes(p.brand));

  const checkedGenders = Array.from(document.querySelectorAll('[data-filter="gender"]:checked')).map(cb => cb.value);
  if (checkedGenders.length) products = products.filter(p => checkedGenders.includes(p.gender) || (checkedGenders.includes('mens') && p.gender === 'unisex'));

  const checkedTypes = Array.from(document.querySelectorAll('[data-filter="type"]:checked')).map(cb => cb.value);
  if (checkedTypes.length) products = products.filter(p => checkedTypes.includes(p.type));

  const checkedMaterials = Array.from(document.querySelectorAll('[data-filter="material"]:checked')).map(cb => cb.value);
  if (checkedMaterials.length) products = products.filter(p => checkedMaterials.includes(p.material));

  const checkedColors = Array.from(document.querySelectorAll('[data-filter="color"]:checked')).map(cb => cb.value);
  if (checkedColors.length) products = products.filter(p => checkedColors.includes(p.color));

  const checkedFeatures = Array.from(document.querySelectorAll('[data-filter="feature"]:checked')).map(cb => cb.value);
  if (checkedFeatures.length) products = products.filter(p => checkedFeatures.every(f => p.feature.includes(f)));

  const minPrice = document.getElementById('price-min')?.value;
  const maxPrice = document.getElementById('price-max')?.value;
  if (minPrice) products = products.filter(p => p.price >= parseInt(minPrice));
  if (maxPrice) products = products.filter(p => p.price <= parseInt(maxPrice));

  // Sort
  const sort = document.getElementById('sort-select')?.value || 'popular';
  if (sort === 'price-asc') products.sort((a,b) => a.price - b.price);
  else if (sort === 'price-desc') products.sort((a,b) => b.price - a.price);
  else if (sort === 'newest') products.sort((a,b) => (a.isNew === b.isNew ? 0 : a.isNew ? -1 : 1));
  else if (sort === 'discount') products.sort((a,b) => b.discount - a.discount);

  renderProducts('products-container', products);
  const countEl = document.getElementById('results-count');
  if (countEl) countEl.textContent = products.length + ' محصول';
}

function setupTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.tab-panel');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tab.dataset.tab).classList.add('active');
    });
  });
}

function setupFAQ() {
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
      q.parentElement.classList.toggle('active');
    });
  });
}

function renderCart() {
  const container = document.getElementById('cart-items');
  const summary = document.getElementById('cart-summary');
  if (!container) return;

  if (Store.cart.length === 0) {
    container.innerHTML = `<div class="empty-state"><h3>سبد خرید خالی است</h3><p>محصولاتی که دوست دارید را به سبد اضافه کنید</p><a href="../index.html" class="btn-primary">ادامه خرید</a></div>`;
    if (summary) summary.style.display = 'none';
    return;
  }

  container.innerHTML = Store.cart.map(item => `
    <div class="cart-item">
      <img src="${item.image}" alt="${item.name}">
      <div class="cart-item-info">
        <h4>${item.name}</h4>
        <p>${item.brandFa}</p>
        <div class="quantity-selector" style="margin-top:10px;width:fit-content">
          <button onclick="updateCartQty(${item.id},-1)">-</button>
          <input type="text" value="${item.qty}" readonly>
          <button onclick="updateCartQty(${item.id},1)">+</button>
        </div>
      </div>
      <div style="text-align:left">
        <div class="cart-item-price">${formatPrice(item.price * item.qty)}</div>
        <button onclick="Store.removeFromCart(${item.id})" style="margin-top:10px;background:none;border:none;color:var(--primary);cursor:pointer;font-family:inherit">حذف</button>
      </div>
    </div>
  `).join('');

  const total = Store.getCartTotal();
  const shipping = total > 75000000 ? 0 : 350000;
  if (summary) {
    summary.style.display = 'block';
    summary.innerHTML = `
      <h3>خلاصه سفارش</h3>
      <div class="summary-row"><span>مجموع کالاها</span><span>${formatPrice(total)}</span></div>
      <div class="summary-row"><span>هزینه ارسال</span><span>${shipping === 0 ? 'رایگان' : formatPrice(shipping)}</span></div>
      <div class="summary-row total"><span>مبلغ قابل پرداخت</span><span>${formatPrice(total + shipping)}</span></div>
      ${total < 75000000 ? `<p style="font-size:12px;color:var(--text-light);margin-top:10px">${formatPrice(75000000 - total)} تا ارسال رایگان</p>` : ''}
      <a href="../checkout/index.html" class="btn-primary" style="width:100%;margin-top:20px;justify-content:center">ادامه فرآیند خرید</a>
    `;
  }
}

function updateCartQty(id, delta) {
  const item = Store.cart.find(i => i.id === id);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) Store.removeFromCart(id);
  else { Store.save(); renderCart(); }
}

function renderWishlist() {
  const container = document.getElementById('wishlist-container');
  if (!container) return;
  if (Store.wishlist.length === 0) {
    container.innerHTML = `<div class="empty-state"><h3>لیست علاقه‌مندی‌ها خالی است</h3><p>محصولات مورد علاقه خود را اینجا ذخیره کنید</p><a href="../index.html" class="btn-primary">مشاهده محصولات</a></div>`;
    return;
  }
  container.innerHTML = `<div class="products-grid">${Store.wishlist.map(renderProductCard).join('')}</div>`;
}

function renderCompare() {
  const container = document.getElementById('compare-container');
  if (!container) return;
  if (Store.compare.length === 0) {
    container.innerHTML = `<div class="empty-state"><h3>لیست مقایسه خالی است</h3><p>محصولات را برای مقایسه انتخاب کنید</p><a href="../index.html" class="btn-primary">مشاهده محصولات</a></div>`;
    return;
  }
  const specs = ['brandFa','price','gender','type','material','color'];
  const specLabels = {'brandFa':'برند','price':'قیمت','gender':'جنسیت','type':'نوع موتور','material':'متریال بند','color':'رنگ'};
  const genderMap = {'mens':'مردانه','ladies':'زنانه','unisex':'یونیسکس','couple':'ست'};

  let html = '<table class="compare-table"><thead><tr><th>ویژگی</th>';
  Store.compare.forEach(p => {
    html += `<th><img src="${p.image}" class="compare-product-img"><div>${p.name}</div><button onclick="Store.toggleCompare(DB.products.find(x=>x.id===${p.id}))" style="margin-top:10px;background:none;border:none;color:var(--primary);cursor:pointer">حذف</button></th>`;
  });
  html += '</tr></thead><tbody>';
  specs.forEach(spec => {
    html += `<tr><td>${specLabels[spec]}</td>`;
    Store.compare.forEach(p => {
      let val = p[spec];
      if (spec === 'price') val = formatPrice(val);
      if (spec === 'gender') val = genderMap[val] || val;
      html += `<td>${val}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

function setupSearch() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      window.location.href = '../watch/index.html?q=' + encodeURIComponent(searchInput.value);
    }
  });
}

async function initHomepage() {
  let products = DB.products;
  try { products = await API.Products.list({ limit: 50 }); } catch(e) {}
  renderProducts('best-sellers', products.filter(p => p.rating >= 4.7).slice(0, 4));
  renderProducts('new-arrivals', DB.products.filter(p => p.isNew).slice(0, 4));
  renderProducts('discounted', DB.products.filter(p => p.discount > 0).slice(0, 4));

  const brandsContainer = document.getElementById('brands-container');
  if (brandsContainer) {
    brandsContainer.innerHTML = DB.brands.map(b => `
      <a href="watch/index.html?brand=${b.name}" class="brand-card">${b.nameFa}</a>
    `).join('');
  }

  const blogContainer = document.getElementById('blog-container');
  if (blogContainer) {
    blogContainer.innerHTML = DB.articles.slice(0, 3).map(renderBlogCard).join('');
  }
}

function initListingPage() {
  setupFilters();
  setupSearch();
  applyFilters();
}

function initProductDetail() {
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'));
  const product = DB.products.find(p => p.id === id);
  if (!product) return;

  Store.addViewed(product);

  document.getElementById('detail-name').textContent = product.name;
  document.getElementById('detail-brand').textContent = product.brandFa;
  document.getElementById('detail-image').src = product.image;
  document.getElementById('detail-price').innerHTML = `
    <span class="current">${formatPrice(product.price)}</span>
    ${product.oldPrice ? `<span class="old">${formatPrice(product.oldPrice)}</span>` : ''}
  `;
  document.getElementById('detail-stock').textContent = product.stock > 0 ? '✅ موجود در انبار' : '❌ ناموجود';

  const specsTable = document.getElementById('detail-specs');
  if (specsTable) {
    const specMap = {movement:'نوع موتور', diameter:'قطر صفحه', thickness:'ضخامت', case:'جنس قاب', band:'جنس بند', glass:'نوع شیشه', water:'مقاومت در برابر آب', weight:'وزن', functions:'امکانات'};
    specsTable.innerHTML = Object.entries(product.specs).map(([k,v]) => `
      <tr><td>${specMap[k] || k}</td><td>${v}</td></tr>
    `).join('');
  }

  document.getElementById('btn-add-cart').onclick = () => Store.addToCart(product, parseInt(document.getElementById('detail-qty')?.value || 1));
  document.getElementById('btn-add-wish').onclick = () => Store.toggleWishlist(product);

  const related = DB.products.filter(p => p.brand === product.brand && p.id !== product.id).slice(0, 4);
  renderProducts('related-products', related);
  setupTabs();
}

function initMagazine() {
  const container = document.getElementById('magazine-container');
  if (container) container.innerHTML = DB.articles.map(renderBlogCard).join('');
}

function initMagazineDetail() {
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'));
  const article = DB.articles.find(a => a.id === id);
  if (!article) return;
  document.getElementById('article-title').textContent = article.title;
  document.getElementById('article-image').src = article.image;
  document.getElementById('article-date').textContent = article.date;
  document.getElementById('article-author').textContent = article.author;
  document.getElementById('article-category').textContent = article.category;
}

function initCheckout() {
  const total = Store.getCartTotal();
  const shipping = total > 75000000 ? 0 : 350000;
  document.getElementById('checkout-total').textContent = formatPrice(total + shipping);
}
