/* ============================================
   DOT WATCH - Main JavaScript
   Dynamic E-commerce Functionality
   ============================================ */

// ===== Global State =====
const AppState = {
    cart: JSON.parse(localStorage.getItem('dotwatch_cart')) || [],
    wishlist: JSON.parse(localStorage.getItem('dotwatch_wishlist')) || [],
    compare: JSON.parse(localStorage.getItem('dotwatch_compare')) || [],
    recentViews: JSON.parse(localStorage.getItem('dotwatch_recent')) || [],
    user: JSON.parse(localStorage.getItem('dotwatch_user')) || null,
    isLoggedIn: localStorage.getItem('dotwatch_auth') === 'true'
};

// ===== DOM Ready =====
document.addEventListener('DOMContentLoaded', function() {
    initHeader();
    initSlider();
    initCart();
    initWishlist();
    initTabs();
    initMobileMenu();
    initScrollAnimations();
    initSearch();
    updateHeaderCounts();
});

// ===== Header & Navigation =====
function initHeader() {
    // Sticky header shadow on scroll
    const header = document.querySelector('.header-main');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.style.boxShadow = '0 4px 30px rgba(0,0,0,0.15)';
            } else {
                header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
            }
        });
    }
}

function initMobileMenu() {
    // Mobile menu toggle would go here
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('mobile-open');
        });
    }
}

// ===== Hero Slider =====
function initSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');

    if (slides.length === 0) return;

    let currentSlide = 0;
    const totalSlides = slides.length;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }

    // Auto slide
    let slideInterval = setInterval(nextSlide, 5000);

    // Dot click
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            clearInterval(slideInterval);
            currentSlide = index;
            showSlide(currentSlide);
            slideInterval = setInterval(nextSlide, 5000);
        });
    });
}

// ===== Cart Management =====
function initCart() {
    document.querySelectorAll('.btn-add-cart').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const card = this.closest('.product-card') || this.closest('.product-detail-info');
            if (!card) return;

            const product = {
                id: card.dataset.id || Math.random().toString(36).substr(2, 9),
                name: card.querySelector('.product-title, h1')?.textContent?.trim() || 'محصول',
                brand: card.querySelector('.product-brand')?.textContent?.trim() || '',
                price: parseInt(card.querySelector('.price-current, .current')?.textContent?.replace(/[^0-9]/g, '')) || 0,
                oldPrice: parseInt(card.querySelector('.price-old, .old')?.textContent?.replace(/[^0-9]/g, '')) || 0,
                image: card.querySelector('img')?.src || '',
                quantity: 1
            };

            addToCart(product);
        });
    });

    // Cart page specific
    initCartPage();
}

function addToCart(product) {
    const existing = AppState.cart.find(item => item.id === product.id);
    if (existing) {
        existing.quantity += 1;
    } else {
        AppState.cart.push(product);
    }
    saveCart();
    updateHeaderCounts();
    showNotification('محصول به سبد خرید اضافه شد', 'success');
}

function removeFromCart(productId) {
    AppState.cart = AppState.cart.filter(item => item.id !== productId);
    saveCart();
    updateHeaderCounts();
    renderCartItems();
    updateCartSummary();
}

function updateCartQuantity(productId, quantity) {
    const item = AppState.cart.find(item => item.id === productId);
    if (item) {
        item.quantity = Math.max(1, quantity);
        saveCart();
        updateHeaderCounts();
        renderCartItems();
        updateCartSummary();
    }
}

function saveCart() {
    localStorage.setItem('dotwatch_cart', JSON.stringify(AppState.cart));
}

function initCartPage() {
    renderCartItems();
    updateCartSummary();
}

function renderCartItems() {
    const container = document.querySelector('.cart-items');
    if (!container) return;

    if (AppState.cart.length === 0) {
        container.innerHTML = `
            <div style="padding: 60px 20px; text-align: center;">
                <i class="fas fa-shopping-cart" style="font-size: 60px; color: #e5e7eb; margin-bottom: 20px;"></i>
                <h3 style="margin-bottom: 10px;">سبد خرید شما خالی است</h3>
                <p style="color: #6b7280; margin-bottom: 20px;">محصولات مورد علاقه خود را به سبد خرید اضافه کنید</p>
                <a href="/watch/index.html" class="btn btn-primary">مشاهده محصولات</a>
            </div>
        `;
        return;
    }

    container.innerHTML = AppState.cart.map(item => `
        <div class="cart-item" data-id="${item.id}">
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <p>${item.brand}</p>
            </div>
            <div class="quantity-selector">
                <button onclick="updateCartQuantity('${item.id}', ${item.quantity - 1})">−</button>
                <input type="text" value="${item.quantity}" readonly>
                <button onclick="updateCartQuantity('${item.id}', ${item.quantity + 1})">+</button>
            </div>
            <div class="cart-item-price">${(item.price * item.quantity).toLocaleString()} تومان</div>
            <div class="cart-item-remove" onclick="removeFromCart('${item.id}')">
                <i class="fas fa-trash-alt"></i>
            </div>
        </div>
    `).join('');
}

function updateCartSummary() {
    const subtotalEl = document.getElementById('cart-subtotal');
    const totalEl = document.getElementById('cart-total');
    const shippingEl = document.getElementById('cart-shipping');

    if (!subtotalEl) return;

    const subtotal = AppState.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const shipping = subtotal > 750000 ? 0 : 45000;
    const total = subtotal + shipping;

    subtotalEl.textContent = subtotal.toLocaleString() + ' تومان';
    if (shippingEl) shippingEl.textContent = shipping === 0 ? 'رایگان' : shipping.toLocaleString() + ' تومان';
    if (totalEl) totalEl.textContent = total.toLocaleString() + ' تومان';

    // Free shipping progress
    const progressBar = document.querySelector('.progress-bar .fill');
    const progressText = document.querySelector('.free-shipping-bar p');
    if (progressBar && progressText) {
        const remaining = Math.max(0, 750000 - subtotal);
        const percent = Math.min(100, (subtotal / 750000) * 100);
        progressBar.style.width = percent + '%';
        if (remaining > 0) {
            progressText.innerHTML = `${remaining.toLocaleString()} تومان تا ارسال <span>رایگان</span>`;
        } else {
            progressText.innerHTML = 'شما از <span>ارسال رایگان</span> برخوردار شدید!';
        }
    }
}

// ===== Wishlist Management =====
function initWishlist() {
    document.querySelectorAll('.btn-wishlist').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const card = this.closest('.product-card');
            if (!card) return;

            const product = {
                id: card.dataset.id || Math.random().toString(36).substr(2, 9),
                name: card.querySelector('.product-title')?.textContent?.trim() || 'محصول',
                brand: card.querySelector('.product-brand')?.textContent?.trim() || '',
                price: parseInt(card.querySelector('.price-current')?.textContent?.replace(/[^0-9]/g, '')) || 0,
                image: card.querySelector('img')?.src || ''
            };

            toggleWishlist(product);
        });
    });
}

function toggleWishlist(product) {
    const index = AppState.wishlist.findIndex(item => item.id === product.id);
    if (index > -1) {
        AppState.wishlist.splice(index, 1);
        showNotification('از لیست علاقه‌مندی‌ها حذف شد', 'info');
    } else {
        AppState.wishlist.push(product);
        showNotification('به لیست علاقه‌مندی‌ها اضافه شد', 'success');
    }
    localStorage.setItem('dotwatch_wishlist', JSON.stringify(AppState.wishlist));
    updateHeaderCounts();
}

// ===== Compare Management =====
function addToCompare(product) {
    if (AppState.compare.length >= 4) {
        showNotification('حداکثر 4 محصول قابل مقایسه است', 'error');
        return;
    }
    if (!AppState.compare.find(item => item.id === product.id)) {
        AppState.compare.push(product);
        localStorage.setItem('dotwatch_compare', JSON.stringify(AppState.compare));
        showNotification('به لیست مقایسه اضافه شد', 'success');
    }
}

// ===== Header Counts =====
function updateHeaderCounts() {
    const cartBadge = document.querySelector('.header-action .badge[data-type="cart"]');
    const wishlistBadge = document.querySelector('.header-action .badge[data-type="wishlist"]');

    if (cartBadge) {
        const count = AppState.cart.reduce((sum, item) => sum + item.quantity, 0);
        cartBadge.textContent = count;
        cartBadge.style.display = count > 0 ? 'flex' : 'none';
    }

    if (wishlistBadge) {
        const count = AppState.wishlist.length;
        wishlistBadge.textContent = count;
        wishlistBadge.style.display = count > 0 ? 'flex' : 'none';
    }
}

// ===== Tabs =====
function initTabs() {
    const tabNavs = document.querySelectorAll('.tab-nav');

    tabNavs.forEach(nav => {
        const buttons = nav.querySelectorAll('button');
        const contents = nav.parentElement.querySelectorAll('.tab-content');

        buttons.forEach((btn, index) => {
            btn.addEventListener('click', () => {
                buttons.forEach(b => b.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                if (contents[index]) contents[index].classList.add('active');
            });
        });
    });
}

// ===== Search =====
function initSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (!searchInput) return;

    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        if (query.length < 2) return;

        // Simulate search suggestions
        // In a real app, this would fetch from server
    });
}

// ===== Notification =====
function showNotification(message, type = 'success') {
    // Remove existing notifications
    document.querySelectorAll('.notification').forEach(n => n.remove());

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    // Trigger animation
    requestAnimationFrame(() => {
        notification.classList.add('show');
    });

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 400);
    }, 3000);
}

// ===== Scroll Animations =====
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.product-card, .blog-card, .category-card, .value-card').forEach(el => {
        observer.observe(el);
    });
}

// ===== Countdown Timer =====
function initCountdown() {
    const countdownEl = document.querySelector('.countdown');
    if (!countdownEl) return;

    let hours = 5, minutes = 32, seconds = 45;

    setInterval(() => {
        seconds--;
        if (seconds < 0) { seconds = 59; minutes--; }
        if (minutes < 0) { minutes = 59; hours--; }
        if (hours < 0) { hours = 23; }

        const h = countdownEl.querySelector('.hours');
        const m = countdownEl.querySelector('.minutes');
        const s = countdownEl.querySelector('.seconds');

        if (h) h.textContent = String(hours).padStart(2, '0');
        if (m) m.textContent = String(minutes).padStart(2, '0');
        if (s) s.textContent = String(seconds).padStart(2, '0');
    }, 1000);
}

// ===== Product Gallery =====
function initProductGallery() {
    const mainImage = document.querySelector('.main-image img');
    const thumbnails = document.querySelectorAll('.thumbnail-images img');

    if (!mainImage || thumbnails.length === 0) return;

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', () => {
            mainImage.src = thumb.src;
            thumbnails.forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        });
    });
}

// ===== Checkout Form =====
function initCheckout() {
    const form = document.querySelector('.checkout-form form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        showNotification('سفارش شما با موفقیت ثبت شد', 'success');
        AppState.cart = [];
        saveCart();
        updateHeaderCounts();
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
    });
}

// ===== Contact Form =====
function initContactForm() {
    const form = document.querySelector('.contact-form-card form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        showNotification('پیام شما با موفقیت ارسال شد', 'success');
        form.reset();
    });
}

// ===== Auth =====
function login(email, password) {
    // Simulate login
    AppState.user = { email, name: 'کاربر دات واچ' };
    AppState.isLoggedIn = true;
    localStorage.setItem('dotwatch_auth', 'true');
    localStorage.setItem('dotwatch_user', JSON.stringify(AppState.user));
    showNotification('ورود با موفقیت انجام شد', 'success');
    setTimeout(() => window.location.href = 'index.html', 1000);
}

function logout() {
    AppState.user = null;
    AppState.isLoggedIn = false;
    localStorage.removeItem('dotwatch_auth');
    localStorage.removeItem('dotwatch_user');
    showNotification('خروج از حساب کاربری', 'info');
    setTimeout(() => window.location.href = 'index.html', 1000);
}

// ===== Admin Panel Functions =====
const AdminAPI = {
    products: JSON.parse(localStorage.getItem('admin_products')) || [],
    orders: JSON.parse(localStorage.getItem('admin_orders')) || [],
    users: JSON.parse(localStorage.getItem('admin_users')) || [],
    categories: JSON.parse(localStorage.getItem('admin_categories')) || [],
    brands: JSON.parse(localStorage.getItem('admin_brands')) || [],

    save(key, data) {
        localStorage.setItem('admin_' + key, JSON.stringify(data));
        this[key] = data;
    },

    addProduct(product) {
        product.id = Date.now().toString();
        product.createdAt = new Date().toISOString();
        this.products.push(product);
        this.save('products', this.products);
        return product;
    },

    updateProduct(id, data) {
        const index = this.products.findIndex(p => p.id === id);
        if (index > -1) {
            this.products[index] = { ...this.products[index], ...data };
            this.save('products', this.products);
        }
    },

    deleteProduct(id) {
        this.products = this.products.filter(p => p.id !== id);
        this.save('products', this.products);
    },

    addCategory(category) {
        category.id = Date.now().toString();
        this.categories.push(category);
        this.save('categories', this.categories);
    },

    deleteCategory(id) {
        this.categories = this.categories.filter(c => c.id !== id);
        this.save('categories', this.categories);
    },

    addBrand(brand) {
        brand.id = Date.now().toString();
        this.brands.push(brand);
        this.save('brands', this.brands);
    },

    deleteBrand(id) {
        this.brands = this.brands.filter(b => b.id !== id);
        this.save('brands', this.brands);
    },

    updateOrderStatus(id, status) {
        const order = this.orders.find(o => o.id === id);
        if (order) {
            order.status = status;
            this.save('orders', this.orders);
        }
    },

    getStats() {
        return {
            totalProducts: this.products.length,
            totalOrders: this.orders.length,
            totalUsers: this.users.length,
            totalRevenue: this.orders.reduce((sum, o) => sum + (o.total || 0), 0),
            pendingOrders: this.orders.filter(o => o.status === 'pending').length,
            deliveredOrders: this.orders.filter(o => o.status === 'delivered').length
        };
    }
};

// Initialize demo data for admin
function initAdminData() {
    if (AdminAPI.products.length === 0) {
        const demoProducts = [
            { id: '1', name: 'ساعت مچی مردانه کاسیو G-Shock', brand: 'Casio', price: 4500000, oldPrice: 5200000, category: 'watch', subcategory: 'mens', stock: 15, image: '', status: 'active' },
            { id: '2', name: 'ساعت مچی زنانه سیتیزن Eco-Drive', brand: 'Citizen', price: 3800000, oldPrice: 0, category: 'watch', subcategory: 'ladies', stock: 8, image: '', status: 'active' },
            { id: '3', name: 'ساعت مچی مردانه سیکو 5', brand: 'Seiko', price: 2900000, oldPrice: 3500000, category: 'watch', subcategory: 'mens', stock: 12, image: '', status: 'active' },
            { id: '4', name: 'گردنبند نقره زنانه', brand: 'Jowissa', price: 850000, oldPrice: 0, category: 'jewelry', subcategory: 'necklaces', stock: 20, image: '', status: 'active' },
            { id: '5', name: 'دکمه سردست مردانه', brand: 'Viceroy', price: 450000, oldPrice: 0, category: 'accessory', subcategory: 'cufflinks', stock: 30, image: '', status: 'active' }
        ];
        AdminAPI.save('products', demoProducts);
    }

    if (AdminAPI.categories.length === 0) {
        AdminAPI.save('categories', [
            { id: '1', name: 'ساعت مچی', slug: 'watch', parent: null },
            { id: '2', name: 'زیورآلات', slug: 'jewelry', parent: null },
            { id: '3', name: 'اکسسوری', slug: 'accessory', parent: null },
            { id: '4', name: 'ساعت مردانه', slug: 'mens', parent: '1' },
            { id: '5', name: 'ساعت زنانه', slug: 'ladies', parent: '1' }
        ]);
    }

    if (AdminAPI.brands.length === 0) {
        AdminAPI.save('brands', [
            { id: '1', name: 'Casio', slug: 'casio' },
            { id: '2', name: 'Seiko', slug: 'seiko' },
            { id: '3', name: 'Citizen', slug: 'citizen' },
            { id: '4', name: 'Orient', slug: 'orient' },
            { id: '5', name: 'Omax', slug: 'omax' }
        ]);
    }

    if (AdminAPI.orders.length === 0) {
        AdminAPI.save('orders', [
            { id: 'ORD-001', customer: 'علی محمدی', total: 4500000, status: 'pending', date: '1403/05/15' },
            { id: 'ORD-002', customer: 'سارا احمدی', total: 3800000, status: 'delivered', date: '1403/05/12' },
            { id: 'ORD-003', customer: 'رضا کریمی', total: 7200000, status: 'processing', date: '1403/05/14' }
        ]);
    }

    if (AdminAPI.users.length === 0) {
        AdminAPI.save('users', [
            { id: '1', name: 'علی محمدی', email: 'ali@example.com', phone: '09123456789', orders: 5 },
            { id: '2', name: 'سارا احمدی', email: 'sara@example.com', phone: '09129876543', orders: 3 }
        ]);
    }
}

// Call init on admin pages
if (document.querySelector('.admin-panel')) {
    initAdminData();
}

// ===== Utility Functions =====
function formatPrice(price) {
    return price.toLocaleString('fa-IR') + ' تومان';
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('fa-IR');
}

function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

// Export for global access
window.AppState = AppState;
window.AdminAPI = AdminAPI;
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.updateCartQuantity = updateCartQuantity;
window.toggleWishlist = toggleWishlist;
window.addToCompare = addToCompare;
window.showNotification = showNotification;
window.login = login;
window.logout = logout;
window.formatPrice = formatPrice;
window.initCountdown = initCountdown;
window.initProductGallery = initProductGallery;
window.initCheckout = initCheckout;
window.initContactForm = initContactForm;
