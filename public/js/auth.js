// ==================== DOTWATCH USER AUTH v5 — DYNAMIC =======================
(function(){
'use strict';

var scripts = document.querySelectorAll('script[src*="auth.js"]');
var thisScript = scripts[scripts.length - 1];
var scriptSrc = thisScript ? thisScript.getAttribute('src') : './js/auth.js';
var prefix = './';
if (scriptSrc.indexOf('/') !== -1) {
  var parts = scriptSrc.split('/');
  parts.pop(); parts.pop();
  if (parts.length > 0) prefix = parts.join('/') + '/';
}

// ── Demo Data ──
function initDemoData() {
  if (!localStorage.getItem('dotwatch_user')) {
    var demoUser = {
      id: 1001,
      name: 'علی احمدی',
      email: 'ali.ahmadi@example.com',
      phone: '09123456789',
      birthdate: '1375-03-15',
      nationalId: '0012345678',
      avatar: 'ع ا',
      role: 'user',
      createdAt: new Date().toISOString(),
      password: btoa('123456')
    };
    localStorage.setItem('dotwatch_user', JSON.stringify(demoUser));

    var demoAddresses = [
      { id: 1, title: '🏠 خانه', province: 'تهران', city: 'تهران', address: 'خیابان جمهوری، پلاک ۱۲۳، واحد ۴', postalCode: '1334567890', receiver: 'علی احمدی', phone: '09123456789', isDefault: true },
      { id: 2, title: '🏢 محل کار', province: 'تهران', city: 'تهران', address: 'خیابان ولیعصر، برج میلاد، طبقه ۱۲', postalCode: '1549876543', receiver: 'علی احمدی', phone: '09123456789', isDefault: false }
    ];
    localStorage.setItem('dotwatch_addresses', JSON.stringify(demoAddresses));

    var demoOrders = [
      { id: 1026, date: '1405/05/20', items: [{name: 'ساعت کاسیو ادیفایس', qty: 1, price: 4850000}], total: 4850000, status: 'delivered', statusFa: '✅ تحویل داده شده', color: '#28a745' },
      { id: 1025, date: '1405/05/15', items: [{name: 'ساعت فسیل جیانا', qty: 1, price: 3200000}, {name: 'دکمه سردست نقره‌ای', qty: 2, price: 1700000}], total: 4900000, status: 'delivered', statusFa: '✅ تحویل داده شده', color: '#28a745' },
      { id: 1024, date: '1405/05/10', items: [{name: 'ساعت سیکو ۵ اسپرت', qty: 1, price: 8900000}], total: 8900000, status: 'shipping', statusFa: '🚚 در حال ارسال', color: 'orange' }
    ];
    localStorage.setItem('dotwatch_orders', JSON.stringify(demoOrders));

    var demoNotifications = [
      { id: 1, title: 'سفارش شما ارسال شد', message: 'سفارش #۱۰۲۴ از طریق پست پیشتاز ارسال شد.', time: '۲ ساعت پیش', read: false },
      { id: 2, title: 'تخفیف ویژه جی‌شاک', message: '۲۰٪ تخفیف ویژه ساعت‌های جی‌شاک تا پایان هفته', time: 'دیروز', read: false },
      { id: 3, title: 'به دات واچ خوش آمدید', message: 'از اینکه به جمع ما پیوستید سپاسگزاریم.', time: '۳ روز پیش', read: true }
    ];
    localStorage.setItem('dotwatch_notifications', JSON.stringify(demoNotifications));
  }
}
initDemoData();

var AUTH_CSS = [
  '.user-account-wrapper{position:relative;display:inline-block}',
  '.user-account-btn{display:flex;align-items:center;gap:8px;padding:6px 14px;border:1px solid #e0e0e0;border-radius:50px;background:#fff;cursor:pointer;transition:all .3s;font-family:inherit;color:#333;font-size:13px}',
  '.user-account-btn:hover{border-color:#c9a96e;box-shadow:0 2px 12px rgba(0,0,0,.08)}',
  '.user-avatar{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}',
  '.user-name{font-size:13px;font-weight:500;white-space:nowrap;max-width:110px;overflow:hidden;text-overflow:ellipsis}',
  '.user-dropdown-menu{position:absolute;top:calc(100% + 12px);right:0;min-width:280px;background:#fff;border-radius:16px;box-shadow:0 12px 48px rgba(0,0,0,.18);padding:10px 0;opacity:0;visibility:hidden;transform:translateY(-8px);transition:all .25s cubic-bezier(.4,0,.2,1);z-index:99999;border:1px solid rgba(0,0,0,.06);pointer-events:none}',
  '.user-dropdown-menu.show{opacity:1;visibility:visible;transform:translateY(0);pointer-events:auto}',
  '.user-dropdown-menu::before{content:"";position:absolute;top:-6px;right:28px;width:12px;height:12px;background:#fff;transform:rotate(45deg);border-top:1px solid rgba(0,0,0,.06);border-right:1px solid rgba(0,0,0,.06)}',
  '.user-dropdown-header{display:flex;align-items:center;gap:12px;padding:18px 22px 14px}',
  '.user-avatar-large{width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:700;flex-shrink:0}',
  '.user-info{display:flex;flex-direction:column;gap:3px;overflow:hidden;direction:rtl;text-align:right}',
  '.user-name-large{font-size:15px;font-weight:600;color:#333;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
  '.user-detail-row{font-size:12px;color:#888;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:6px}',
  '.user-detail-row svg{width:14px;height:14px;opacity:.6;flex-shrink:0}',
  '.user-dropdown-divider{height:1px;background:linear-gradient(to right,transparent,#e8e8e8,transparent);margin:6px 18px}',
  '.user-dropdown-item{display:flex;align-items:center;gap:12px;padding:12px 22px;color:#444;text-decoration:none;font-size:14px;transition:all .15s;cursor:pointer;background:none;border:none;width:100%;font-family:inherit;text-align:right;direction:rtl}',
  '.user-dropdown-item:hover{background:rgba(201,169,110,.08);color:#c9a96e}',
  '.user-dropdown-item svg{flex-shrink:0;opacity:.65}',
  '.user-dropdown-item:hover svg{opacity:1}',
  '.user-logout-btn{color:#e74c3c}',
  '.user-logout-btn:hover{background:rgba(231,76,60,.08);color:#e74c3c}',
  '@media(max-width:768px){.user-name{display:none}.user-account-btn{padding:6px}.user-dropdown-menu{min-width:240px}}'
].join('');

var st = document.createElement('style');
st.textContent = AUTH_CSS;
document.head.appendChild(st);

var UserAuth = {
  getUser: function() {
    try {
      var u = localStorage.getItem('dotwatch_user');
      return u ? JSON.parse(u) : null;
    } catch(e) { return null; }
  },

  isLoggedIn: function() {
    return !!this.getUser();
  },

  register: function(userData) {
    var user = {
      id: userData.id || Date.now(),
      name: userData.name || 'کاربر',
      email: userData.email || '',
      phone: userData.phone || '',
      birthdate: userData.birthdate || '',
      nationalId: userData.nationalId || '',
      avatar: userData.avatar || this.generateAvatar(userData.name || 'کاربر'),
      role: userData.role || 'user',
      createdAt: userData.createdAt || new Date().toISOString(),
      password: userData.password ? btoa(userData.password) : ''
    };
    localStorage.setItem('dotwatch_user', JSON.stringify(user));
    // Initialize empty collections
    if (!localStorage.getItem('dotwatch_addresses')) localStorage.setItem('dotwatch_addresses', '[]');
    if (!localStorage.getItem('dotwatch_orders')) localStorage.setItem('dotwatch_orders', '[]');
    if (!localStorage.getItem('dotwatch_notifications')) localStorage.setItem('dotwatch_notifications', '[]');
    this.renderUserAccount();
    if (typeof showNotification === 'function') {
      showNotification('ثبت نام با موفقیت انجام شد! خوش آمدید ' + user.name + ' 👋');
    }
    return user;
  },

  login: function(credentials) {
    var user = this.getUser();
    if (!user) return { success: false, message: 'کاربری یافت نشد. لطفاً ابتدا ثبت نام کنید.' };
    var id = (credentials.id || '').trim();
    var password = credentials.password || '';
    var match = (user.phone === id || user.email === id);
    var passMatch = user.password === btoa(password);
    if (match && passMatch) {
      localStorage.setItem('dotwatch_session', JSON.stringify({ userId: user.id, loginAt: new Date().toISOString() }));
      this.renderUserAccount();
      if (typeof showNotification === 'function') {
        showNotification('خوش آمدید ' + user.name + ' 👋');
      }
      return { success: true, user: user };
    }
    return { success: false, message: 'شماره موبایل/ایمیل یا رمز عبور اشتباه است.' };
  },

  logout: function() {
    localStorage.removeItem('dotwatch_session');
    this.renderUserAccount();
    if (typeof showNotification === 'function') {
      showNotification('با موفقیت خارج شدید');
    }
    setTimeout(function() {
      var p = window.location.pathname;
      if (p.indexOf('profile') !== -1 || p.indexOf('orders') !== -1 || p.indexOf('addresses') !== -1) {
        window.location.href = prefix + 'index.html';
      }
    }, 500);
  },

  updateProfile: function(data) {
    var user = this.getUser();
    if (!user) return null;
    Object.keys(data).forEach(function(key) {
      if (key !== 'id' && key !== 'createdAt') {
        user[key] = data[key];
      }
    });
    if (data.name) user.avatar = this.generateAvatar(data.name);
    localStorage.setItem('dotwatch_user', JSON.stringify(user));
    this.renderUserAccount();
    return user;
  },

  changePassword: function(oldPass, newPass) {
    var user = this.getUser();
    if (!user) return false;
    if (user.password !== btoa(oldPass)) return false;
    user.password = btoa(newPass);
    localStorage.setItem('dotwatch_user', JSON.stringify(user));
    return true;
  },

  // ── Addresses ──
  getAddresses: function() {
    try {
      return JSON.parse(localStorage.getItem('dotwatch_addresses') || '[]');
    } catch(e) { return []; }
  },

  addAddress: function(addr) {
    var list = this.getAddresses();
    addr.id = Date.now();
    if (addr.isDefault) {
      list.forEach(function(a) { a.isDefault = false; });
    }
    list.push(addr);
    localStorage.setItem('dotwatch_addresses', JSON.stringify(list));
    return addr;
  },

  updateAddress: function(id, addr) {
    var list = this.getAddresses();
    var idx = list.findIndex(function(a) { return a.id == id; });
    if (idx === -1) return null;
    if (addr.isDefault) {
      list.forEach(function(a) { a.isDefault = false; });
    }
    list[idx] = Object.assign({}, list[idx], addr);
    localStorage.setItem('dotwatch_addresses', JSON.stringify(list));
    return list[idx];
  },

  deleteAddress: function(id) {
    var list = this.getAddresses();
    list = list.filter(function(a) { return a.id != id; });
    localStorage.setItem('dotwatch_addresses', JSON.stringify(list));
    return list;
  },

  // ── Orders ──
  getOrders: function() {
    try {
      return JSON.parse(localStorage.getItem('dotwatch_orders') || '[]');
    } catch(e) { return []; }
  },

  addOrder: function(order) {
    var list = this.getOrders();
    order.id = order.id || ('#' + (1000 + list.length + 1));
    list.unshift(order);
    localStorage.setItem('dotwatch_orders', JSON.stringify(list));
    return order;
  },

  // ── Notifications ──
  getNotifications: function() {
    try {
      return JSON.parse(localStorage.getItem('dotwatch_notifications') || '[]');
    } catch(e) { return []; }
  },

  markNotificationRead: function(id) {
    var list = this.getNotifications();
    var n = list.find(function(x) { return x.id == id; });
    if (n) n.read = true;
    localStorage.setItem('dotwatch_notifications', JSON.stringify(list));
  },

  addNotification: function(notif) {
    var list = this.getNotifications();
    notif.id = Date.now();
    notif.read = false;
    list.unshift(notif);
    if (list.length > 20) list.pop();
    localStorage.setItem('dotwatch_notifications', JSON.stringify(list));
  },

  generateAvatar: function(name) {
    if (!name) return '';
    var p = name.trim().split(' ').filter(Boolean);
    if (p.length >= 2) return p[0][0] + p[1][0];
    return name.substring(0, 2);
  },

  formatPhone: function(phone) {
    if (!phone) return '';
    var p = phone.replace(/\D/g, '');
    if (p.length === 11 && p.charAt(0) === '0') {
      return p.substring(0, 4) + ' ' + p.substring(4, 7) + ' ' + p.substring(7, 9) + ' ' + p.substring(9, 11);
    }
    return phone;
  },

  toPersianDate: function(dateStr) {
    if (!dateStr) return '';
    var parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    return parts[0] + '/' + parts[1] + '/' + parts[2];
  },

  toggleDropdown: function(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    var d = document.querySelector('.user-dropdown-menu');
    if (!d) return;
    var isOpen = d.classList.contains('show');
    document.querySelectorAll('.user-dropdown-menu').forEach(function(m) { m.classList.remove('show'); });
    if (!isOpen) d.classList.add('show');
  },

  closeDropdown: function() {
    document.querySelectorAll('.user-dropdown-menu').forEach(function(m) { m.classList.remove('show'); });
  },

  renderUserAccount: function() {
    var c = document.getElementById('user-account-container');
    if (!c) return;
    var user = this.getUser();
    if (user) {
      var phoneDisplay = user.phone ? this.formatPhone(user.phone) : '';
      var emailDisplay = user.email || '';
      var birthDisplay = user.birthdate ? this.toPersianDate(user.birthdate) : '';

      var infoHtml = '';
      if (phoneDisplay) {
        infoHtml += '<div class="user-detail-row"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>' + phoneDisplay + '</span></div>';
      }
      if (emailDisplay) {
        infoHtml += '<div class="user-detail-row"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><span>' + emailDisplay + '</span></div>';
      }
      if (birthDisplay) {
        infoHtml += '<div class="user-detail-row"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg><span>' + birthDisplay + '</span></div>';
      }

      c.innerHTML = '<div class="user-account-wrapper">' +
        '<button class="user-account-btn" id="ua-toggle" aria-label="منوی کاربر">' +
          '<div class="user-avatar">' + (user.avatar || this.generateAvatar(user.name)) + '</div>' +
          '<span class="user-name">' + user.name + '</span>' +
          '<svg class="user-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' +
        '</button>' +
        '<div class="user-dropdown-menu" id="ua-menu">' +
          '<div class="user-dropdown-header">' +
            '<div class="user-avatar-large">' + (user.avatar || this.generateAvatar(user.name)) + '</div>' +
            '<div class="user-info">' +
              '<span class="user-name-large">' + user.name + '</span>' +
              infoHtml +
            '</div>' +
          '</div>' +
          '<div class="user-dropdown-divider"></div>' +
          '<a href="' + prefix + 'profile/index.html" class="user-dropdown-item">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>' +
            '<span>پروفایل</span>' +
          '</a>' +
          '<a href="' + prefix + 'profile/index.html#orders" class="user-dropdown-item">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>' +
            '<span>سفارش‌های من</span>' +
          '</a>' +
          '<a href="' + prefix + 'profile/index.html#addresses" class="user-dropdown-item">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>' +
            '<span>آدرس‌ها</span>' +
          '</a>' +
          '<div class="user-dropdown-divider"></div>' +
          '<button class="user-dropdown-item user-logout-btn" id="ua-logout">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>' +
            '<span>خروج از حساب</span>' +
          '</button>' +
        '</div>' +
      '</div>';
      var btn = c.querySelector('#ua-toggle');
      var logoutBtn = c.querySelector('#ua-logout');
      if (btn) btn.addEventListener('click', function(e) { UserAuth.toggleDropdown(e); });
      if (logoutBtn) logoutBtn.addEventListener('click', function() { UserAuth.logout(); });
    } else {
      c.innerHTML = '<a href="' + prefix + 'login/index.html" class="action-btn">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>' +
        '<span>ورود</span>' +
      '</a>' +
      '<a href="' + prefix + 'register/index.html" class="action-btn">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>' +
        '<span>ثبت نام</span>' +
      '</a>';
    }
  },

  init: function() {
    this.renderUserAccount();
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.user-account-wrapper')) UserAuth.closeDropdown();
    });
  }
};

window.UserAuth = UserAuth;

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() { UserAuth.init(); });
} else {
  UserAuth.init();
}
})();