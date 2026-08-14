// DotWatch API Bridge - Connects old frontend to new backend
// Include this file AFTER data.js and BEFORE app.js in your HTML

const API_BASE = window.API_BASE || 'http://localhost:3000/api';
let authToken = localStorage.getItem('dw_token') || '';

async function api(url, opts = {}) {
  const res = await fetch(API_BASE + url, {
    headers: {
      'Content-Type': 'application/json',
      ...(authToken ? { 'Authorization': 'Bearer ' + authToken } : {})
    },
    ...opts
  });
  if (res.status === 401) { localStorage.removeItem('dw_token'); authToken = ''; }
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// ========== AUTH BRIDGE ==========
const Auth = {
  async register(data) {
    const r = await api('/auth/register', { method: 'POST', body: JSON.stringify(data) });
    if (r.token) { authToken = r.token; localStorage.setItem('dw_token', r.token); }
    return r;
  },
  async login(email, password) {
    const r = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });
    if (r.token) { authToken = r.token; localStorage.setItem('dw_token', r.token); }
    return r;
  },
  async me() {
    if (!authToken) return null;
    try { return await api('/auth/me'); } catch { return null; }
  },
  logout() {
    authToken = ''; localStorage.removeItem('dw_token');
  }
};

// ========== PRODUCTS BRIDGE ==========
const Products = {
  async list(params = {}) {
    const q = new URLSearchParams(params).toString();
    return api('/products?' + q);
  },
  async get(id) {
    return api('/products/' + id);
  }
};

// ========== CART BRIDGE ==========
const CartAPI = {
  async get() {
    if (!authToken) return Store.cart;
    const items = await api('/cart');
    Store.cart = items.map(i => ({
      id: i.product_id, name: i.name, brandFa: i.brandFa,
      price: i.price, image: i.image, qty: i.qty
    }));
    Store.save();
    return Store.cart;
  },
  async add(product, qty = 1) {
    if (!authToken) { Store.addToCart(product, qty); return; }
    await api('/cart', { method: 'POST', body: JSON.stringify({ product_id: product.id, qty }) });
    Store.addToCart(product, qty);
  },
  async remove(id) {
    if (!authToken) { Store.removeFromCart(id); return; }
    await api('/cart/' + id, { method: 'DELETE' });
    Store.removeFromCart(id);
  },
  async updateQty(id, qty) {
    if (!authToken) {
      const item = Store.cart.find(i => i.id === id);
      if (item) { item.qty = qty; if (item.qty <= 0) Store.removeFromCart(id); else Store.save(); }
      return;
    }
    await api('/cart/' + id, { method: 'PUT', body: JSON.stringify({ qty }) });
    const item = Store.cart.find(i => i.id === id);
    if (item) { item.qty = qty; Store.save(); }
  }
};

// ========== WISHLIST BRIDGE ==========
const WishlistAPI = {
  async get() {
    if (!authToken) return Store.wishlist;
    const items = await api('/wishlist');
    Store.wishlist = items.map(i => ({
      id: i.product_id, name: i.name, brandFa: i.brandFa,
      price: i.price, image: i.image
    }));
    Store.save();
    return Store.wishlist;
  },
  async toggle(product) {
    if (!authToken) { Store.toggleWishlist(product); return; }
    try {
      await api('/wishlist', { method: 'POST', body: JSON.stringify({ product_id: product.id }) });
      Store.toggleWishlist(product);
    } catch { Store.toggleWishlist(product); }
  }
};

// ========== ORDERS BRIDGE ==========
const OrdersAPI = {
  async create(items, address, note) {
    const payload = {
      items: items.map(i => ({ product_id: i.id, name: i.name, image: i.image, price: i.price, qty: i.qty })),
      shipping_address: address,
      note
    };
    return api('/orders', { method: 'POST', body: JSON.stringify(payload) });
  },
  async list() {
    return api('/orders');
  }
};

// ========== ADMIN BRIDGE ==========
const AdminAPI = {
  async getData() {
    return api('/admin/data');
  },
  async saveProduct(product) {
    const method = product.id ? 'PUT' : 'POST';
    const url = product.id ? '/products/' + product.id : '/products';
    return api(url, { method, body: JSON.stringify(product) });
  },
  async deleteProduct(id) {
    return api('/products/' + id, { method: 'DELETE' });
  },
  async updateOrderStatus(id, status) {
    return api('/orders/' + id + '/status', { method: 'PUT', body: JSON.stringify({ status }) });
  },
  async updateUser(id, data) {
    return api('/users/' + id, { method: 'PUT', body: JSON.stringify(data) });
  },
  async saveBanner(banner) {
    const method = banner.id ? 'PUT' : 'POST';
    const url = banner.id ? '/banners/' + banner.id : '/banners';
    return api(url, { method, body: JSON.stringify(banner) });
  },
  async deleteBanner(id) {
    return api('/banners/' + id, { method: 'DELETE' });
  },
  async saveMenu(menu) {
    const method = menu.id ? 'PUT' : 'POST';
    const url = menu.id ? '/menus/' + menu.id : '/menus';
    return api(url, { method, body: JSON.stringify(menu) });
  },
  async saveFooterLink(link) {
    const method = link.id ? 'PUT' : 'POST';
    const url = link.id ? '/footer-links/' + link.id : '/footer-links';
    return api(url, { method, body: JSON.stringify(link) });
  },
  async saveText(section, key, value) {
    return api('/page-texts', { method: 'PUT', body: JSON.stringify({ section, key_name: key, value }) });
  },
  async saveSettings(settings) {
    return api('/settings', { method: 'PUT', body: JSON.stringify(settings) });
  },
  async backup() {
    return api('/admin/backup');
  }
};

// ========== SYNC ON LOAD ==========
(async function initBridge() {
  if (authToken) {
    try {
      await CartAPI.get();
      await WishlistAPI.get();
    } catch (e) { console.log('Bridge sync:', e.message); }
  }
})();

// Expose globally
window.API = { Auth, Products, Cart: CartAPI, Wishlist: WishlistAPI, Orders: OrdersAPI, Admin: AdminAPI, api };
