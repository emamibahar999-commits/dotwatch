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

const Auth = {
  async register(d) {
    const r = await api('/auth/register', { method: 'POST', body: JSON.stringify(d) });
    if (r.token) { authToken = r.token; localStorage.setItem('dw_token', r.token); }
    return r;
  },
  async login(e, p) {
    const r = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email: e, password: p }) });
    if (r.token) { authToken = r.token; localStorage.setItem('dw_token', r.token); }
    return r;
  },
  async me() {
    if (!authToken) return null;
    try { return await api('/auth/me'); } catch { return null; }
  },
  logout() { authToken = ''; localStorage.removeItem('dw_token'); }
};

const Products = {
  async list(p = {}) {
    const q = new URLSearchParams(p).toString();
    return api('/products?' + q);
  },
  async get(id) { return api('/products/' + id); }
};

const CartAPI = {
  async get() {
    if (!authToken) return Store.cart;
    const items = await api('/cart');
    Store.cart = items.map(i => ({ id: i.product_id, name: i.name, brandFa: i.brandFa, price: i.price, image: i.image, qty: i.qty }));
    Store.save(); return Store.cart;
  },
  async add(product, qty = 1) {
    if (!authToken) { Store.addToCart(product, qty); return; }
    await api('/cart', { method: 'POST', body: JSON.stringify({ product_id: product.id, qty }) });
    Store.addToCart(product, qty);
  },
  async remove(id) {
    if (!authToken) { Store.removeFromCart(id); return; }
    await api('/cart/' + id, { method: 'DELETE' }); Store.removeFromCart(id);
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

const WishlistAPI = {
  async get() {
    if (!authToken) return Store.wishlist;
    const items = await api('/wishlist');
    Store.wishlist = items.map(i => ({ id: i.product_id, name: i.name, brandFa: i.brandFa, price: i.price, image: i.image }));
    Store.save(); return Store.wishlist;
  },
  async toggle(product) {
    if (!authToken) { Store.toggleWishlist(product); return; }
    try {
      await api('/wishlist', { method: 'POST', body: JSON.stringify({ product_id: product.id }) });
      Store.toggleWishlist(product);
    } catch { Store.toggleWishlist(product); }
  }
};

const OrdersAPI = {
  async create(items, address, note) {
    return api('/orders', { method: 'POST', body: JSON.stringify({
      items: items.map(i => ({ product_id: i.id, name: i.name, image: i.image, price: i.price, qty: i.qty })),
      shipping_address: address, note
    })});
  },
  async list() { return api('/orders'); }
};

const AdminAPI = {
  async getData() { return api('/admin/data'); },
  async saveProduct(p) {
    const m = p.id ? 'PUT' : 'POST';
    const u = p.id ? '/products/' + p.id : '/products';
    return api(u, { method: m, body: JSON.stringify(p) });
  },
  async deleteProduct(id) { return api('/products/' + id, { method: 'DELETE' }); },
  async updateOrderStatus(id, s) { return api('/orders/' + id + '/status', { method: 'PUT', body: JSON.stringify({ status: s }) }); },
  async updateUser(id, d) { return api('/users/' + id, { method: 'PUT', body: JSON.stringify(d) }); },
  async saveBanner(b) {
    const m = b.id ? 'PUT' : 'POST';
    const u = b.id ? '/banners/' + b.id : '/banners';
    return api(u, { method: m, body: JSON.stringify(b) });
  },
  async deleteBanner(id) { return api('/banners/' + id, { method: 'DELETE' }); },
  async saveMenu(m) {
    const mt = m.id ? 'PUT' : 'POST';
    const u = m.id ? '/menus/' + m.id : '/menus';
    return api(u, { method: mt, body: JSON.stringify(m) });
  },
  async saveFooterLink(l) {
    const m = l.id ? 'PUT' : 'POST';
    const u = l.id ? '/footer-links/' + l.id : '/footer-links';
    return api(u, { method: m, body: JSON.stringify(l) });
  },
  async saveText(sec, key, val) {
    return api('/page-texts', { method: 'PUT', body: JSON.stringify({ section: sec, key_name: key, value: val }) });
  },
  async saveSettings(s) { return api('/settings', { method: 'PUT', body: JSON.stringify(s) }); },
  async backup() { return api('/admin/backup'); }
};

(async function init() {
  if (authToken) { try { await CartAPI.get(); await WishlistAPI.get(); } catch (e) {} }
})();

window.API = { Auth, Products, Cart: CartAPI, Wishlist: WishlistAPI, Orders: OrdersAPI, Admin: AdminAPI, api };
