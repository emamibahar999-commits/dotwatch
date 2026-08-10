#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_all_auth.py
===============
این اسکریپت یکجا همه فایل‌های مربوط به ورود/ثبت‌نام/پروفایل رو اصلاح می‌کنه.

فایل‌هایی که جایگزین می‌شن:
  1. js/auth.js         → دکمه ورود + ثبت نام وقتی لاگین نیستی + ذخیره رمز
  2. login/index.html   → فرم ورود با چک کردن رمز عبور
  3. register/index.html→ فرم ثبت‌نام با ذخیره رمز + تکرار رمز
  4. profile/index.html → داینامیک، خواندن از dotwatch_user

نحوه اجرا:
    python3 fix_all_auth.py

بعد از اجرا Ctrl+F5 بزن تو مرورگر.
"""

import os

AUTH_JS = r"""// ========== DOTWATCH USER AUTH v5.1 (FULLY FIXED) ==========
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
  '.auth-guest{display:flex;align-items:center;gap:6px}',
  '.auth-guest .action-btn{padding:6px 14px;border:1px solid #e0e0e0;border-radius:50px;background:#fff;font-size:13px;color:#333;text-decoration:none;display:flex;align-items:center;gap:6px;transition:all .3s;font-family:inherit}',
  '.auth-guest .action-btn:hover{border-color:#c9a96e;color:#c9a96e}',
  '.auth-guest .action-btn.primary{background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;border:none}',
  '.auth-guest .action-btn.primary:hover{box-shadow:0 4px 12px rgba(201,169,110,.3)}',
  '@media(max-width:768px){.user-name{display:none}.user-account-btn{padding:6px}.user-dropdown-menu{min-width:240px}.auth-guest .action-btn span{display:none}}'
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

  login: function(userData) {
    var user = {
      id: userData.id || Date.now(),
      name: userData.name || 'کاربر',
      email: userData.email || '',
      phone: userData.phone || '',
      password: userData.password || '',
      birthdate: userData.birthdate || '',
      avatar: userData.avatar || this.generateAvatar(userData.name || 'کاربر'),
      role: userData.role || 'user',
      createdAt: userData.createdAt || new Date().toISOString()
    };
    localStorage.setItem('dotwatch_user', JSON.stringify(user));
    try {
      var users = JSON.parse(localStorage.getItem('dotwatch_users') || '[]');
      var existing = users.find(function(u) { return u.phone === user.phone || u.email === user.email; });
      if (existing) { Object.assign(existing, user); }
      else { users.push(user); }
      localStorage.setItem('dotwatch_users', JSON.stringify(users));
    } catch(e) {}
    this.renderUserAccount();
    if (typeof showNotification === 'function') {
      showNotification('خوش آمدید ' + user.name + ' 🎉');
    }
    return user;
  },

  logout: function() {
    localStorage.removeItem('dotwatch_user');
    localStorage.removeItem('dotwatch_currentUser');
    localStorage.removeItem('dotwatch_isLoggedIn');
    this.renderUserAccount();
    if (typeof showNotification === 'function') {
      showNotification('شما خارج شدید');
    }
    setTimeout(function() {
      var p = window.location.pathname;
      if (p.indexOf('profile') !== -1 || p.indexOf('orders') !== -1 || p.indexOf('addresses') !== -1) {
        window.location.href = prefix + 'index.html';
      }
    }, 500);
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
      var birthDisplay = user.birthdate || '';
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
        '<button class="user-account-btn" id="ua-toggle" aria-label="حساب کاربری">' +
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
            '<span>حساب کاربری</span>' +
          '</a>' +
          '<a href="' + prefix + 'profile/index.html#orders" class="user-dropdown-item">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>' +
            '<span>سفارشات من</span>' +
          '</a>' +
          '<a href="' + prefix + 'profile/index.html#addresses" class="user-dropdown-item">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>' +
            '<span>آدرس‌ها</span>' +
          '</a>' +
          '<a href="' + prefix + 'wishlist/index.html" class="user-dropdown-item">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>' +
            '<span>علاقه‌مندی‌ها</span>' +
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
      c.innerHTML = '<div class="auth-guest">' +
        '<a href="' + prefix + 'login/index.html" class="action-btn">' +
          '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>' +
          '<span>ورود</span>' +
        '</a>' +
        '<a href="' + prefix + 'register/index.html" class="action-btn primary">' +
          '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>' +
          '<span>ثبت نام</span>' +
        '</a>' +
      '</div>';
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
"""

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ورود | دات واچ</title>
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .auth-section { padding: 60px 20px; background: linear-gradient(135deg, #f9f6f1 0%, #fff 100%); min-height: 70vh; display: flex; align-items: center; justify-content: center; }
    .auth-box { width: 100%; max-width: 420px; background: #fff; border-radius: 24px; padding: 40px 36px; box-shadow: 0 20px 60px rgba(0,0,0,0.06); border: 1px solid #f0ebe3; }
    .auth-title { text-align: center; font-size: 22px; font-weight: 700; margin-bottom: 8px; color: #2c2c2c; }
    .auth-subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 32px; }
    .form-group { margin-bottom: 22px; }
    .form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 8px; color: #555; }
    .form-group input { width: 100%; padding: 14px 16px; border: 1px solid #e5e0d8; border-radius: 12px; font-size: 14px; font-family: inherit; transition: all 0.3s; background: #fdfcfa; }
    .form-group input:focus { outline: none; border-color: #c9a96e; background: #fff; box-shadow: 0 0 0 3px rgba(201,169,110,0.1); }
    .form-group input.error { border-color: #e74c3c; background: #fff5f5; }
    .btn-submit { width: 100%; padding: 15px; border: none; border-radius: 12px; background: linear-gradient(135deg, #c9a96e, #a08050); color: #fff; font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer; transition: all 0.3s; margin-top: 6px; }
    .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(201,169,110,0.35); }
    .btn-submit:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }
    .auth-error { color: #e74c3c; font-size: 13px; text-align: center; margin-bottom: 16px; display: none; padding: 10px; background: #fff5f5; border-radius: 8px; }
    .auth-error.show { display: block; }
    .auth-success { color: #27ae60; font-size: 13px; text-align: center; margin-bottom: 16px; display: none; padding: 10px; background: #f0fff4; border-radius: 8px; }
    .auth-success.show { display: block; }
    .auth-foot { text-align: center; margin-top: 28px; padding-top: 24px; border-top: 1px solid #f0ebe3; font-size: 14px; color: #777; }
    .auth-foot a { color: #c9a96e; text-decoration: none; font-weight: 600; }
    .auth-foot a:hover { text-decoration: underline; }
    .spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid #fff; border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; vertical-align: middle; margin-left: 8px; }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
<div class="top-bar"><div class="container">🎁 ارسال رایگان برای خرید بالای ۷۵۰ هزار تومان | <a href="../discounts/index.html">مشاهده تخفیفات</a></div></div>
<header class="header">
  <div class="container">
    <div class="header-main">
      <a href="../index.html" class="logo"><div class="logo-icon">⌚</div><span>دات واچ</span></a>
      <div class="search-box">
        <input type="text" id="search-input" placeholder="جستجوی ساعت، برند، مدل...">
        <button onclick="const v=document.getElementById('search-input').value;if(v)window.location.href='../watch/index.html?q='+encodeURIComponent(v)">🔍</button>
      </div>
      <div class="header-actions">
        <a href="../cart/index.html" class="action-btn"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg><span>سبد خرید</span></a>
        <div id="user-account-container"></div>
      </div>
      <button class="mobile-toggle" onclick="document.querySelector('.nav-menu').classList.toggle('active')">☰</button>
    </div>
  </div>
  <nav class="nav">
    <div class="container">
      <ul class="nav-menu">
        <li class="nav-item"><a href="../index.html" class="nav-link">صفحه اصلی</a></li>
        <li class="nav-item"><a href="../watch/index.html" class="nav-link">ساعت مچی ⌚</a></li>
        <li class="nav-item"><a href="../accessory/index.html" class="nav-link">اکسسوری ⌚</a></li>
        <li class="nav-item"><a href="../brands/index.html" class="nav-link">برندها</a></li>
        <li class="nav-item"><a href="../discounts/index.html" class="nav-link">🔥 تخفیفات</a></li>
        <li class="nav-item"><a href="../best-sellers/index.html" class="nav-link">⭐ پرفروش‌ترین‌ها</a></li>
        <li class="nav-item"><a href="../daily-deals/index.html" class="nav-link">⚡ پیشنهاد امروز</a></li>
        <li class="nav-item"><a href="../magazine/index.html" class="nav-link">📰 مجله</a></li>
        <li class="nav-item"><a href="../contact/index.html" class="nav-link">📞 تماس با ما</a></li>
      </ul>
    </div>
  </nav>
</header>

<main class="auth-section">
  <div class="auth-box">
    <h1 class="auth-title">ورود به حساب</h1>
    <p class="auth-subtitle">وارد حساب کاربری خود شوید</p>
    <div class="auth-error" id="login-error">کاربری با این مشخصات یافت نشد</div>
    <div class="auth-success" id="login-success">ورود موفق! در حال انتقال...</div>
    <form id="login-form" novalidate>
      <div class="form-group">
        <label>شماره موبایل یا ایمیل</label>
        <input type="text" id="login-id" placeholder="شماره موبایل یا ایمیل خود را وارد کنید" required>
      </div>
      <div class="form-group">
        <label>رمز عبور</label>
        <input type="password" id="login-password" placeholder="رمز عبور خود را وارد کنید" required minlength="6">
      </div>
      <button type="submit" class="btn-submit" id="login-btn">ورود</button>
    </form>
    <div class="auth-foot">حساب کاربری ندارید؟ <a href="./register.html">ثبت نام کنید</a></div>
  </div>
</main>

<footer class="footer" style="background:#1a1a1a;color:#fff;padding:50px 0 20px;margin-top:0">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:40px;margin-bottom:40px">
      <div><h4 style="color:#c9a96e;margin-bottom:20px;font-size:18px">دات واچ</h4><p style="color:#aaa;font-size:14px;line-height:1.8">فروشگاه تخصصی ساعت‌های مچی و اکسسوری با بهترین برندهای جهانی</p></div>
      <div><h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">دسترسی سریع</h4><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="../watch/index.html" style="color:#aaa;text-decoration:none;font-size:14px">ساعت مچی</a></li><li style="margin-bottom:10px"><a href="../brands/index.html" style="color:#aaa;text-decoration:none;font-size:14px">برندها</a></li><li style="margin-bottom:10px"><a href="../discounts/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تخفیفات</a></li></ul></div>
      <div><h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">پشتیبانی</h4><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="../faq/index.html" style="color:#aaa;text-decoration:none;font-size:14px">سوالات متداول</a></li><li style="margin-bottom:10px"><a href="../rules/index.html" style="color:#aaa;text-decoration:none;font-size:14px">قوانین</a></li><li style="margin-bottom:10px"><a href="../contact/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تماس با ما</a></li></ul></div>
    </div>
    <div style="border-top:1px solid #333;padding-top:20px;text-align:center;color:#777;font-size:13px">© ۱۴۰۴ دات واچ. تمامی حقوق محفوظ است.</div>
  </div>
</footer>

<script src="../js/auth.js"></script>
<script>
(function() {
  'use strict';
  if (localStorage.getItem('dotwatch_user')) {
    try { var u = JSON.parse(localStorage.getItem('dotwatch_user')); if (u && u.name) { window.location.href = '../index.html'; return; } } catch(e) {}
  }
  function normalizePhone(phone) { return phone.replace(/\D/g, ''); }
  function findUser(users, identifier) {
    var id = identifier.trim(); var idNum = normalizePhone(id);
    for (var i = 0; i < users.length; i++) {
      var u = users[i];
      if (u.email && u.email.trim() === id) return u;
      if (u.phone) { var up = normalizePhone(u.phone); if (up === idNum || u.phone.trim() === id) return u; }
    } return null;
  }
  function getAllUsers() {
    var users = [];
    try { var raw = localStorage.getItem('dotwatch_users'); if (raw) users = JSON.parse(raw); } catch(e) {}
    if (users.length === 0) { try { var single = localStorage.getItem('dotwatch_user'); if (single) users.push(JSON.parse(single)); } catch(e) {} }
    return users;
  }
  function saveUsers(users) { localStorage.setItem('dotwatch_users', JSON.stringify(users)); }
  var form = document.getElementById('login-form');
  var btn = document.getElementById('login-btn');
  var errBox = document.getElementById('login-error');
  var succBox = document.getElementById('login-success');
  var idInput = document.getElementById('login-id');
  var passInput = document.getElementById('login-password');
  function showError(msg) { errBox.textContent = msg; errBox.classList.add('show'); succBox.classList.remove('show'); }
  function hideError() { errBox.classList.remove('show'); }
  function showSuccess() { succBox.classList.add('show'); errBox.classList.remove('show'); }
  form.addEventListener('submit', function(e) {
    e.preventDefault(); hideError();
    var identifier = idInput.value.trim();
    var password = passInput.value;
    if (!identifier) { idInput.classList.add('error'); showError('لطفاً شماره موبایل یا ایمیل را وارد کنید'); return; }
    idInput.classList.remove('error');
    if (!password || password.length < 6) { passInput.classList.add('error'); showError('رمز عبور باید حداقل ۶ کاراکتر باشد'); return; }
    passInput.classList.remove('error');
    btn.disabled = true; var originalText = btn.innerHTML; btn.innerHTML = 'در حال ورود... <span class="spinner"></span>';
    setTimeout(function() {
      var users = getAllUsers();
      var user = findUser(users, identifier);
      if (!user) { showError('کاربری با این شماره موبایل یا ایمیل یافت نشد'); btn.disabled = false; btn.innerHTML = originalText; return; }
      if (!user.password) { user.password = password; for (var i = 0; i < users.length; i++) { if (users[i].id === user.id) users[i] = user; } saveUsers(users); localStorage.setItem('dotwatch_user', JSON.stringify(user)); }
      else if (user.password !== password) { showError('رمز عبور اشتباه است'); btn.disabled = false; btn.innerHTML = originalText; return; }
      localStorage.setItem('dotwatch_user', JSON.stringify(user));
      localStorage.setItem('dotwatch_currentUser', JSON.stringify(user));
      localStorage.setItem('dotwatch_isLoggedIn', 'true');
      showSuccess();
      setTimeout(function() { window.location.href = '../index.html'; }, 800);
    }, 600);
  });
  idInput.addEventListener('input', function() { this.classList.remove('error'); hideError(); });
  passInput.addEventListener('input', function() { this.classList.remove('error'); hideError(); });
})();
</script>
</body>
</html>"""

REGISTER_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ثبت نام | دات واچ</title>
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .auth-section { padding: 60px 20px; background: linear-gradient(135deg, #f9f6f1 0%, #fff 100%); min-height: 70vh; display: flex; align-items: center; justify-content: center; }
    .auth-box { width: 100%; max-width: 460px; background: #fff; border-radius: 24px; padding: 40px 36px; box-shadow: 0 20px 60px rgba(0,0,0,0.06); border: 1px solid #f0ebe3; }
    .auth-title { text-align: center; font-size: 22px; font-weight: 700; margin-bottom: 8px; color: #2c2c2c; }
    .auth-subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 32px; }
    .form-group { margin-bottom: 22px; }
    .form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 8px; color: #555; }
    .form-group label .req { color: #e74c3c; margin-right: 4px; }
    .form-group label .opt { color: #999; font-size: 11px; font-weight: 400; }
    .form-group input, .form-group select { width: 100%; padding: 14px 16px; border: 1px solid #e5e0d8; border-radius: 12px; font-size: 14px; font-family: inherit; transition: all 0.3s; background: #fdfcfa; }
    .form-group input:focus, .form-group select:focus { outline: none; border-color: #c9a96e; background: #fff; box-shadow: 0 0 0 3px rgba(201,169,110,0.1); }
    .form-group input.error, .form-group select.error { border-color: #e74c3c; }
    .bd-row { display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 10px; }
    .err { color: #e74c3c; font-size: 12px; margin-top: 6px; display: none; }
    .err.show { display: block; }
    .btn-submit { width: 100%; padding: 15px; border: none; border-radius: 12px; background: linear-gradient(135deg, #c9a96e, #a08050); color: #fff; font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer; transition: all 0.3s; margin-top: 6px; }
    .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(201,169,110,0.35); }
    .btn-submit:disabled { opacity: 0.7; cursor: not-allowed; }
    .auth-foot { text-align: center; margin-top: 28px; padding-top: 24px; border-top: 1px solid #f0ebe3; font-size: 14px; color: #777; }
    .auth-foot a { color: #c9a96e; text-decoration: none; font-weight: 600; }
    .auth-foot a:hover { text-decoration: underline; }
    .auth-success { color: #27ae60; font-size: 13px; text-align: center; margin-bottom: 16px; display: none; padding: 10px; background: #f0fff4; border-radius: 8px; }
    .auth-success.show { display: block; }
  </style>
</head>
<body>
<div class="top-bar"><div class="container">🎁 ارسال رایگان برای خرید بالای ۷۵۰ هزار تومان | <a href="../discounts/index.html">مشاهده تخفیفات</a></div></div>
<header class="header">
  <div class="container">
    <div class="header-main">
      <a href="../index.html" class="logo"><div class="logo-icon">⌚</div><span>دات واچ</span></a>
      <div class="search-box">
        <input type="text" id="search-input" placeholder="جستجوی ساعت، برند، مدل...">
        <button onclick="const v=document.getElementById('search-input').value;if(v)window.location.href='../watch/index.html?q='+encodeURIComponent(v)">🔍</button>
      </div>
      <div class="header-actions">
        <a href="../cart/index.html" class="action-btn"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg><span>سبد خرید</span></a>
        <div id="user-account-container"></div>
      </div>
      <button class="mobile-toggle" onclick="document.querySelector('.nav-menu').classList.toggle('active')">☰</button>
    </div>
  </div>
  <nav class="nav">
    <div class="container">
      <ul class="nav-menu">
        <li class="nav-item"><a href="../index.html" class="nav-link">صفحه اصلی</a></li>
        <li class="nav-item"><a href="../watch/index.html" class="nav-link">ساعت مچی ⌚</a></li>
        <li class="nav-item"><a href="../accessory/index.html" class="nav-link">اکسسوری ⌚</a></li>
        <li class="nav-item"><a href="../brands/index.html" class="nav-link">برندها</a></li>
        <li class="nav-item"><a href="../discounts/index.html" class="nav-link">🔥 تخفیفات</a></li>
        <li class="nav-item"><a href="../best-sellers/index.html" class="nav-link">⭐ پرفروش‌ترین‌ها</a></li>
        <li class="nav-item"><a href="../daily-deals/index.html" class="nav-link">⚡ پیشنهاد امروز</a></li>
        <li class="nav-item"><a href="../magazine/index.html" class="nav-link">📰 مجله</a></li>
        <li class="nav-item"><a href="../contact/index.html" class="nav-link">📞 تماس با ما</a></li>
      </ul>
    </div>
  </nav>
</header>

<main class="auth-section">
  <div class="auth-box">
    <h1 class="auth-title">ثبت نام</h1>
    <p class="auth-subtitle">حساب کاربری جدید بسازید</p>
    <div class="auth-success" id="reg-success">ثبت‌نام موفق! در حال انتقال...</div>
    <form id="register-form" novalidate>
      <div class="form-group">
        <label>نام و نام خانوادگی <span class="req">*</span></label>
        <input type="text" id="reg-name" placeholder="مثلاً: علی احمدی" required>
        <div class="err" id="err-name">لطفاً نام خود را وارد کنید</div>
      </div>
      <div class="form-group">
        <label>ایمیل <span class="opt">(اختیاری)</span></label>
        <input type="email" id="reg-email" placeholder="example@email.com">
      </div>
      <div class="form-group">
        <label>شماره موبایل <span class="req">*</span></label>
        <input type="tel" id="reg-phone" placeholder="0912xxxxxxx" required>
        <div class="err" id="err-phone">شماره موبایل معتبر نیست</div>
      </div>
      <div class="form-group">
        <label>تاریخ تولد <span class="req">*</span></label>
        <div class="bd-row">
          <select id="reg-day" required><option value="" disabled selected>روز</option></select>
          <select id="reg-month" required>
            <option value="" disabled selected>ماه</option>
            <option value="01">فروردین</option><option value="02">اردیبهشت</option><option value="03">خرداد</option>
            <option value="04">تیر</option><option value="05">مرداد</option><option value="06">شهریور</option>
            <option value="07">مهر</option><option value="08">آبان</option><option value="09">آذر</option>
            <option value="10">دی</option><option value="11">بهمن</option><option value="12">اسفند</option>
          </select>
          <select id="reg-year" required><option value="" disabled selected>سال</option></select>
        </div>
        <div class="err" id="err-birthdate">لطفاً تاریخ تولد را کامل انتخاب کنید</div>
      </div>
      <div class="form-group">
        <label>رمز عبور <span class="req">*</span></label>
        <input type="password" id="reg-password" placeholder="حداقل ۶ کاراکتر" required minlength="6">
        <div class="err" id="err-password">رمز عبور باید حداقل ۶ کاراکتر باشد</div>
      </div>
      <div class="form-group">
        <label>تکرار رمز عبور <span class="req">*</span></label>
        <input type="password" id="reg-password2" placeholder="رمز عبور را تکرار کنید" required>
        <div class="err" id="err-password2">رمز عبور و تکرار آن یکسان نیستند</div>
      </div>
      <button type="submit" class="btn-submit" id="reg-btn">ثبت نام</button>
    </form>
    <div class="auth-foot">قبلاً ثبت نام کردید؟ <a href="./login.html">وارد شوید</a></div>
  </div>
</main>

<footer class="footer" style="background:#1a1a1a;color:#fff;padding:50px 0 20px;margin-top:0">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:40px;margin-bottom:40px">
      <div><h4 style="color:#c9a96e;margin-bottom:20px;font-size:18px">دات واچ</h4><p style="color:#aaa;font-size:14px;line-height:1.8">فروشگاه تخصصی ساعت‌های مچی و اکسسوری با بهترین برندهای جهانی</p></div>
      <div><h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">دسترسی سریع</h4><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="../watch/index.html" style="color:#aaa;text-decoration:none;font-size:14px">ساعت مچی</a></li><li style="margin-bottom:10px"><a href="../brands/index.html" style="color:#aaa;text-decoration:none;font-size:14px">برندها</a></li><li style="margin-bottom:10px"><a href="../discounts/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تخفیفات</a></li></ul></div>
      <div><h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">پشتیبانی</h4><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="../faq/index.html" style="color:#aaa;text-decoration:none;font-size:14px">سوالات متداول</a></li><li style="margin-bottom:10px"><a href="../rules/index.html" style="color:#aaa;text-decoration:none;font-size:14px">قوانین</a></li><li style="margin-bottom:10px"><a href="../contact/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تماس با ما</a></li></ul></div>
    </div>
    <div style="border-top:1px solid #333;padding-top:20px;text-align:center;color:#777;font-size:13px">© ۱۴۰۴ دات واچ. تمامی حقوق محفوظ است.</div>
  </div>
</footer>

<script src="../js/auth.js"></script>
<script>
  var dSel = document.getElementById('reg-day');
  for (var i = 1; i <= 31; i++) { var o = document.createElement('option'); o.value = String(i).padStart(2, '0'); o.textContent = i; dSel.appendChild(o); }
  var ySel = document.getElementById('reg-year');
  var cy = new Date().getFullYear();
  for (var i = cy - 18; i >= cy - 80; i--) { var o = document.createElement('option'); o.value = i; o.textContent = i; ySel.appendChild(o); }
  function validatePhone(phone) { var p = phone.replace(/\D/g, ''); return p.length === 11 && p.charAt(0) === '0'; }
  document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var ok = true;
    var name = document.getElementById('reg-name').value.trim();
    var email = document.getElementById('reg-email').value.trim();
    var phone = document.getElementById('reg-phone').value.trim();
    var day = document.getElementById('reg-day').value;
    var month = document.getElementById('reg-month').value;
    var year = document.getElementById('reg-year').value;
    var pass = document.getElementById('reg-password').value;
    var pass2 = document.getElementById('reg-password2').value;
    document.querySelectorAll('.err').forEach(function(el) { el.classList.remove('show'); });
    document.querySelectorAll('input, select').forEach(function(el) { el.classList.remove('error'); });
    if (!name) { document.getElementById('err-name').classList.add('show'); document.getElementById('reg-name').classList.add('error'); ok = false; }
    if (!validatePhone(phone)) { document.getElementById('err-phone').classList.add('show'); document.getElementById('reg-phone').classList.add('error'); ok = false; }
    if (!day || !month || !year) { document.getElementById('err-birthdate').classList.add('show'); document.querySelectorAll('.bd-row select').forEach(function(el) { el.classList.add('error'); }); ok = false; }
    if (!pass || pass.length < 6) { document.getElementById('err-password').classList.add('show'); document.getElementById('reg-password').classList.add('error'); ok = false; }
    if (pass !== pass2) { document.getElementById('err-password2').classList.add('show'); document.getElementById('reg-password2').classList.add('error'); ok = false; }
    if (!ok) return;
    try {
      var users = JSON.parse(localStorage.getItem('dotwatch_users') || '[]');
      var existing = users.find(function(u) { return u.phone === phone; });
      if (existing) { document.getElementById('err-phone').textContent = 'این شماره قبلاً ثبت شده است'; document.getElementById('err-phone').classList.add('show'); document.getElementById('reg-phone').classList.add('error'); return; }
    } catch(e) {}
    UserAuth.login({ name: name, email: email, phone: phone, birthdate: year + '-' + month + '-' + day, password: pass });
    document.getElementById('reg-success').classList.add('show');
    document.getElementById('reg-btn').disabled = true;
    document.getElementById('reg-btn').textContent = 'ثبت‌نام انجام شد';
    setTimeout(function() { window.location.href = '../index.html'; }, 800);
  });
</script>
</body>
</html>"""

PROFILE_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>حساب کاربری | دات واچ</title>
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .modal-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center; }
    .modal-overlay.active { display:flex; }
    .modal-box { background:#fff; padding:30px; border-radius:16px; width:90%; max-width:500px; box-shadow:0 20px 60px rgba(0,0,0,0.2); }
    .modal-box h3 { margin-bottom:20px; }
    .modal-actions { display:flex; gap:10px; margin-top:20px; justify-content:flex-end; }
    .btn-secondary { background:var(--bg-light); color:var(--text); border:1px solid #ddd; padding:10px 20px; border-radius:8px; cursor:pointer; font-family:inherit; }
    .empty-state { text-align:center; padding:40px; color:var(--text-light); }
    .empty-state svg { width:64px; height:64px; margin-bottom:15px; opacity:0.4; }
    .badge { display:inline-block; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-success { background:#e8f5e9; color:#2e7d32; }
    .badge-warning { background:#fff3e0; color:#ef6c00; }
    .badge-info { background:#e3f2fd; color:#1565c0; }
    .notification-item.unread { border-right:3px solid var(--primary); }
    .address-card { border:2px solid var(--primary); border-radius:12px; padding:20px; margin-bottom:15px; background:#fff8f8; transition:all 0.2s; }
    .address-card:hover { box-shadow:0 4px 12px rgba(0,0,0,0.08); }
    .order-row:hover { background:var(--bg-light); }
    .profile-avatar { width:80px; height:80px; background:var(--primary); color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:32px; margin:0 auto 10px; position:relative; overflow:hidden; }
    .toast { position:fixed; top:20px; left:50%; transform:translateX(-50%) translateY(-100px); background:#333; color:#fff; padding:12px 24px; border-radius:8px; font-size:14px; z-index:99999; transition:transform 0.3s; opacity:0; }
    .toast.show { transform:translateX(-50%) translateY(0); opacity:1; }
    .profile-sidebar .profile-menu a.active { background:var(--primary); color:#fff; }
  </style>
</head>
<body>
<div id="toast" class="toast"></div>
<div class="top-bar"><div class="container">🎁 پیشنهاد ویژه: ارسال رایگان برای خریدهای بالای ۷۵۰ هزار تومان | <a href="../discounts/index.html">مشاهده تخفیفات</a></div></div>
<header class="header">
  <div class="container">
    <div class="header-main">
      <a href="../index.html" class="logo"><div class="logo-icon">◷</div><span>دات واچ</span></a>
      <div class="search-box">
        <input type="text" id="search-input" placeholder="جستجوی ساعت، برند، مدل...">
        <button onclick="const v=document.getElementById('search-input').value;if(v)window.location.href='../watch/index.html?q='+encodeURIComponent(v)">🔍</button>
      </div>
      <div class="header-actions">
        <div id="user-account-container"></div>
        <a href="../cart/index.html" class="action-btn"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg><span>سبد خرید</span></a>
        <a href="../wishlist/index.html" class="action-btn"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg><span>علاقه‌مندی</span></a>
      </div>
      <button class="mobile-toggle" onclick="document.querySelector('.nav-menu').classList.toggle('active')">☰</button>
    </div>
  </div>
  <nav class="nav">
    <div class="container">
      <ul class="nav-menu">
        <li class="nav-item"><a href="../index.html" class="nav-link">صفحه اصلی</a></li>
        <li class="nav-item"><a href="../watch/index.html" class="nav-link">ساعت مچی ▾</a></li>
        <li class="nav-item"><a href="../accessory/index.html" class="nav-link">اکسسوری ▾</a></li>
        <li class="nav-item"><a href="../brands/index.html" class="nav-link">برندها</a></li>
        <li class="nav-item"><a href="../discounts/index.html" class="nav-link">🔥 تخفیفات</a></li>
        <li class="nav-item"><a href="../best-sellers/index.html" class="nav-link">⭐ پرفروش‌ترین‌ها</a></li>
        <li class="nav-item"><a href="../daily-deals/index.html" class="nav-link">⚡ پیشنهاد امروز</a></li>
        <li class="nav-item"><a href="../magazine/index.html" class="nav-link">📰 مجله وومگ</a></li>
        <li class="nav-item"><a href="../contact/index.html" class="nav-link">📞 تماس با ما</a></li>
      </ul>
    </div>
  </nav>
</header>

<div class="page-banner">
  <div class="container">
    <h1>حساب کاربری</h1>
    <div class="breadcrumb"><a href="../index.html">صفحه اصلی</a><span>/</span><span>حساب کاربری</span></div>
  </div>
</div>

<div class="container">
  <div class="profile-layout">
    <aside class="profile-sidebar">
      <div style="text-align:center;margin-bottom:20px">
        <div class="profile-avatar" id="profile-avatar">👤</div>
        <h4 id="sidebar-name">کاربر عزیز</h4>
        <p style="font-size:13px;color:var(--text-light)" id="sidebar-phone">-</p>
      </div>
      <ul class="profile-menu">
        <li><a href="#" class="active" data-tab="info" onclick="showProfileTab('info');return false">👤 اطلاعات شخصی</a></li>
        <li><a href="#" data-tab="addresses" onclick="showProfileTab('addresses');return false">📍 آدرس‌های من</a></li>
        <li><a href="#" data-tab="orders" onclick="showProfileTab('orders');return false">📦 تاریخچه سفارشات</a></li>
        <li><a href="../wishlist/index.html">♥ علاقه‌مندی‌ها</a></li>
        <li><a href="../compare/index.html">⇄ لیست مقایسه</a></li>
        <li><a href="#" data-tab="notifications" onclick="showProfileTab('notifications');return false">🔔 اطلاع‌رسانی‌ها</a></li>
        <li><a href="#" onclick="logout();return false" style="color:var(--primary)">🚪 خروج از حساب</a></li>
      </ul>
    </aside>

    <div id="profile-content">
      <div id="tab-info" class="profile-tab" style="background:#fff;padding:30px;border-radius:16px;box-shadow:var(--shadow);margin-bottom:20px">
        <h3 style="margin-bottom:20px">👤 اطلاعات شخصی</h3>
        <form id="profile-form" onsubmit="saveProfile(event)">
          <div class="form-row">
            <div class="form-group"><label>نام و نام خانوادگی *</label><input type="text" id="p-name" required placeholder="نام خود را وارد کنید"></div>
            <div class="form-group"><label>شماره تماس *</label><input type="tel" id="p-phone" required placeholder="۰۹۱۲۳۴۵۶۷۸۹" pattern="09[0-9]{9}"></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>ایمیل</label><input type="email" id="p-email" placeholder="example@email.com"></div>
            <div class="form-group"><label>تاریخ تولد</label><input type="text" id="p-birthdate" placeholder="۱۳۷۰/۰۱/۰۱"></div>
          </div>
          <button type="submit" class="btn-primary" id="save-profile-btn">💾 ذخیره تغییرات</button>
        </form>
      </div>

      <div id="tab-addresses" class="profile-tab" style="display:none;background:#fff;padding:30px;border-radius:16px;box-shadow:var(--shadow);margin-bottom:20px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <h3>📍 آدرس‌های من</h3>
          <button class="btn-outline" onclick="openAddressModal()">+ افزودن آدرس جدید</button>
        </div>
        <div id="addresses-container"></div>
      </div>

      <div id="tab-orders" class="profile-tab" style="display:none;background:#fff;padding:30px;border-radius:16px;box-shadow:var(--shadow);margin-bottom:20px">
        <h3 style="margin-bottom:20px">📦 تاریخچه سفارشات</h3>
        <div style="overflow-x:auto">
          <table class="specs-table" style="min-width:600px" id="orders-table">
            <thead><tr style="background:var(--bg-light)"><th>شماره سفارش</th><th>تاریخ</th><th>مبلغ</th><th>وضعیت</th><th>عملیات</th></tr></thead>
            <tbody id="orders-tbody"></tbody>
          </table>
        </div>
        <div id="orders-empty" class="empty-state" style="display:none">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
          <p>هنوز سفارشی ثبت نکرده‌اید</p>
          <a href="../watch/index.html" class="btn-primary" style="margin-top:15px;display:inline-block">مشاهده محصولات</a>
        </div>
      </div>

      <div id="tab-notifications" class="profile-tab" style="display:none;background:#fff;padding:30px;border-radius:16px;box-shadow:var(--shadow);margin-bottom:20px">
        <h3 style="margin-bottom:20px">🔔 اطلاع‌رسانی‌ها</h3>
        <div id="notifications-container"></div>
        <div id="notifications-empty" class="empty-state" style="display:none">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
          <p>اعلان جدیدی ندارید</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="modal-overlay" id="address-modal">
  <div class="modal-box">
    <h3 id="address-modal-title">➕ افزودن آدرس جدید</h3>
    <form id="address-form" onsubmit="saveAddress(event)">
      <input type="hidden" id="addr-id">
      <div class="form-group" style="margin-bottom:15px"><label>عنوان آدرس *</label><input type="text" id="addr-title" required placeholder="مثلاً خانه، محل کار"></div>
      <div class="form-group" style="margin-bottom:15px"><label>آدرس کامل *</label><textarea id="addr-full" required rows="3" placeholder="استان، شهر، خیابان، پلاک، واحد" style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px;font-family:inherit"></textarea></div>
      <div class="form-row" style="margin-bottom:15px">
        <div class="form-group"><label>کد پستی</label><input type="text" id="addr-postal" placeholder="۱۲۳۴۵۶۷۸۹۰" pattern="[0-9]{10}"></div>
        <div class="form-group"><label>گیرنده *</label><input type="text" id="addr-recipient" required placeholder="نام و نام خانوادگی گیرنده"></div>
      </div>
      <div class="form-group" style="margin-bottom:15px"><label>شماره تماس گیرنده *</label><input type="tel" id="addr-phone" required placeholder="۰۹۱۲۳۴۵۶۷۸۹" pattern="09[0-9]{9}"></div>
      <div class="modal-actions">
        <button type="button" class="btn-secondary" onclick="closeAddressModal()">انصراف</button>
        <button type="submit" class="btn-primary" id="addr-save-btn">💾 ذخیره</button>
      </div>
    </form>
  </div>
</div>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col"><h4>دات واچ</h4><p style="font-size:14px;line-height:1.8;margin-bottom:15px">مرجع تخصصی نقد و بررسی و خرید اینترنتی ساعت مچی، زیور و اکسسوری اصل</p><div class="social-links"><a href="#">📘</a><a href="#">📸</a><a href="#">🐦</a><a href="#">📺</a></div></div>
      <div class="footer-col"><h4>دسته‌بندی‌ها</h4><ul><li><a href="../watch/mens/index.html">ساعت مردانه</a></li><li><a href="../watch/ladies/index.html">ساعت زنانه</a></li><li><a href="../watch/couple/index.html">ساعت ست</a></li><li><a href="../accessory/index.html">اکسسوری</a></li><li><a href="../magazine/index.html">مجله وومگ</a></li></ul></div>
      <div class="footer-col"><h4>راهنمای خرید</h4><ul><li><a href="../rules/index.html">قوانین و مقررات</a></li><li><a href="../rules/index.html#return">شرایط بازگشت کالا</a></li><li><a href="../rules/index.html#warranty">گارانتی محصولات</a></li><li><a href="../rules/index.html#shipping">نحوه ارسال</a></li><li><a href="../faq/index.html">سوالات متداول</a></li></ul></div>
      <div class="footer-col footer-contact"><h4>تماس با ما</h4><p>📍 تهران، خیابان جمهوری، پلاک ۱۳۳۴</p><p>📞 ۰۲۱-۹۱۰۰۸۰۹۰</p><p>✉️ info@dotwatch.ir</p><p>🕐 شنبه تا پنجشنبه: ۹ صبح تا ۹ شب</p></div>
    </div>
    <div class="footer-bottom"><p>تمامی حقوق محفوظ است © ۱۴۰۴ دات واچ</p></div>
  </div>
</footer>

<script src="../js/auth.js"></script>
<script>
var STORAGE_KEYS = { USER: 'dotwatch_user', ADDRESSES: 'dotwatch_addresses', ORDERS: 'dotwatch_orders', NOTIFICATIONS: 'dotwatch_notifications' };
var DEFAULT_ADDRESSES = [{ id: 'addr_1', title: '🏠 خانه', fullAddress: 'تهران، خیابان جمهوری، پلاک ۱۳۳، واحد ۴', postalCode: '۱۳۳۴۵۶۷۸۹۰', recipient: 'کاربر عزیز', phone: '۰۹۱۲۳۴۵۶۷۸۹' }];
var DEFAULT_ORDERS = [
  { id: '۱۰۲۶', date: '۱۴۰۵/۰۵/۲۰', amount: '۱۲,۵۰۰,۰۰۰ تومان', status: 'delivered', statusText: '✅ تحویل داده شده', items: ['ساعت مچی مردانه رولکس', 'بند چرم اصل'] },
  { id: '۱۰۲۵', date: '۱۴۰۵/۰۵/۱۵', amount: '۸,۹۰۰,۰۰۰ تومان', status: 'delivered', statusText: '✅ تحویل داده شده', items: ['ساعت زنانه کارتیر'] },
  { id: '۱۰۲۴', date: '۱۴۰۵/۰۵/۱۰', amount: '۴,۵۰۰,۰۰۰ تومان', status: 'shipping', statusText: '🚚 در حال ارسال', items: ['ساعت اسپرت گارمین'] }
];
var DEFAULT_NOTIFICATIONS = [
  { id: 'notif_1', title: 'سفارش شما ارسال شد', body: 'سفارش #۱۰۲۶ ارسال شد و به زودی به دست شما می‌رسد.', date: '۲ ساعت پیش', read: false, type: 'order' },
  { id: 'notif_2', title: 'تخفیف ویژه آخر هفته', body: '۲۰٪ تخفیف ویژه روی تمامی ساعت‌های هوشمند تا پایان هفته!', date: 'دیروز', read: true, type: 'promo' }
];
function getStorage(key, defaultVal) { try { var raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : defaultVal; } catch(e) { return defaultVal; } }
function setStorage(key, val) { localStorage.setItem(key, JSON.stringify(val)); }
function showToast(msg) { var t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); setTimeout(function() { t.classList.remove('show'); }, 3000); }
function escapeHtml(text) { if (!text) return ''; var div = document.createElement('div'); div.textContent = text; return div.innerHTML; }
function checkAuth() { var user = getStorage(STORAGE_KEYS.USER, null); if (!user) { window.location.href = '../login/index.html'; return false; } return true; }
function logout() { if (confirm('آیا می‌خواهید از حساب کاربری خارج شوید؟')) { localStorage.removeItem('dotwatch_user'); localStorage.removeItem('dotwatch_currentUser'); localStorage.removeItem('dotwatch_isLoggedIn'); window.location.href = '../index.html'; } }
function renderSidebar() { var user = getStorage(STORAGE_KEYS.USER, null); if (!user) return; document.getElementById('sidebar-name').textContent = user.name || 'کاربر عزیز'; document.getElementById('sidebar-phone').textContent = user.phone || '-'; var avatar = document.getElementById('profile-avatar'); var initial = user.name ? user.name.trim()[0] : '👤'; avatar.textContent = initial; }
function renderProfileInfo() { var user = getStorage(STORAGE_KEYS.USER, null); if (!user) return; document.getElementById('p-name').value = user.name || ''; document.getElementById('p-phone').value = user.phone || ''; document.getElementById('p-email').value = user.email || ''; document.getElementById('p-birthdate').value = user.birthdate || ''; }
function saveProfile(e) { e.preventDefault(); var btn = document.getElementById('save-profile-btn'); btn.innerHTML = '⏳ در حال ذخیره...'; btn.disabled = true; setTimeout(function() { var user = getStorage(STORAGE_KEYS.USER, {}); user.name = document.getElementById('p-name').value.trim(); user.phone = document.getElementById('p-phone').value.trim(); user.email = document.getElementById('p-email').value.trim(); user.birthdate = document.getElementById('p-birthdate').value.trim(); setStorage(STORAGE_KEYS.USER, user); renderSidebar(); showToast('اطلاعات شخصی با موفقیت ذخیره شد ✅'); btn.innerHTML = '💾 ذخیره تغییرات'; btn.disabled = false; if (window.UserAuth) UserAuth.renderUserAccount(); }, 600); }
function renderAddresses() { var container = document.getElementById('addresses-container'); var addresses = getStorage(STORAGE_KEYS.ADDRESSES, DEFAULT_ADDRESSES); if (addresses.length === 0) { container.innerHTML = '<div class="empty-state"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg><p>هنوز آدرسی ثبت نکرده‌اید</p><button class="btn-primary" style="margin-top:15px" onclick="openAddressModal()">+ افزودن آدرس</button></div>'; return; } container.innerHTML = addresses.map(function(addr) { return '<div class="address-card" data-id="' + addr.id + '"><div style="display:flex;justify-content:space-between;margin-bottom:10px;align-items:center"><strong>' + escapeHtml(addr.title) + '</strong><span style="font-size:12px;color:var(--text-light)">' + escapeHtml(addr.postalCode || '') + '</span></div><p style="color:var(--text-light);font-size:14px;line-height:1.7">' + escapeHtml(addr.fullAddress) + '<br>👤 گیرنده: ' + escapeHtml(addr.recipient) + ' | 📞 ' + escapeHtml(addr.phone) + '</p><div style="margin-top:10px"><button style="background:none;border:none;color:var(--primary);cursor:pointer;font-family:inherit;margin-left:15px" onclick="editAddress(\'' + addr.id + '\')">✏️ ویرایش</button><button style="background:none;border:none;color:#e31e24;cursor:pointer;font-family:inherit" onclick="deleteAddress(\'' + addr.id + '\')">🗑️ حذف</button></div></div>'; }).join(''); }
function openAddressModal(editId) { var modal = document.getElementById('address-modal'); var form = document.getElementById('address-form'); var title = document.getElementById('address-modal-title'); form.reset(); document.getElementById('addr-id').value = editId || ''; if (editId) { var addresses = getStorage(STORAGE_KEYS.ADDRESSES, DEFAULT_ADDRESSES); var addr = addresses.find(function(a) { return a.id === editId; }); if (addr) { title.textContent = '✏️ ویرایش آدرس'; document.getElementById('addr-title').value = addr.title.replace(/^[^\s]+\s/, ''); document.getElementById('addr-full').value = addr.fullAddress; document.getElementById('addr-postal').value = addr.postalCode; document.getElementById('addr-recipient').value = addr.recipient; document.getElementById('addr-phone').value = addr.phone; } } else { title.textContent = '➕ افزودن آدرس جدید'; } modal.classList.add('active'); }
function closeAddressModal() { document.getElementById('address-modal').classList.remove('active'); }
function saveAddress(e) { e.preventDefault(); var id = document.getElementById('addr-id').value; var addresses = getStorage(STORAGE_KEYS.ADDRESSES, DEFAULT_ADDRESSES); var newAddr = { id: id || 'addr_' + Date.now(), title: '📍 ' + document.getElementById('addr-title').value.trim(), fullAddress: document.getElementById('addr-full').value.trim(), postalCode: document.getElementById('addr-postal').value.trim(), recipient: document.getElementById('addr-recipient').value.trim(), phone: document.getElementById('addr-phone').value.trim() }; if (id) { var idx = addresses.findIndex(function(a) { return a.id === id; }); if (idx !== -1) addresses[idx] = newAddr; } else { addresses.push(newAddr); } setStorage(STORAGE_KEYS.ADDRESSES, addresses); closeAddressModal(); renderAddresses(); showToast(id ? 'آدرس ویرایش شد ✏️' : 'آدرس جدید افزوده شد ➕'); }
function editAddress(id) { openAddressModal(id); }
function deleteAddress(id) { if (!confirm('آیا از حذف این آدرس اطمینان دارید؟')) return; var addresses = getStorage(STORAGE_KEYS.ADDRESSES, DEFAULT_ADDRESSES).filter(function(a) { return a.id !== id; }); setStorage(STORAGE_KEYS.ADDRESSES, addresses); renderAddresses(); showToast('آدرس حذف شد 🗑️'); }
function renderOrders() { var orders = getStorage(STORAGE_KEYS.ORDERS, DEFAULT_ORDERS); var tbody = document.getElementById('orders-tbody'); var empty = document.getElementById('orders-empty'); var table = document.getElementById('orders-table'); if (orders.length === 0) { table.style.display = 'none'; empty.style.display = 'block'; return; } table.style.display = 'table'; empty.style.display = 'none'; tbody.innerHTML = orders.map(function(order) { var badgeClass = 'badge-info'; if (order.status === 'delivered') badgeClass = 'badge-success'; if (order.status === 'shipping') badgeClass = 'badge-warning'; return '<tr class="order-row"><td><strong>#' + escapeHtml(order.id) + '</strong></td><td>' + escapeHtml(order.date) + '</td><td>' + escapeHtml(order.amount) + '</td><td><span class="badge ' + badgeClass + '">' + escapeHtml(order.statusText) + '</span></td><td><a href="#" style="color:var(--primary)" onclick="showOrderDetail(\'' + order.id + '\');return false">مشاهده</a></td></tr>'; }).join(''); }
function showOrderDetail(orderId) { var orders = getStorage(STORAGE_KEYS.ORDERS, DEFAULT_ORDERS); var order = orders.find(function(o) { return o.id === orderId; }); if (!order) return; alert('جزئیات سفارش #' + order.id + ':\n\n📅 تاریخ: ' + order.date + '\n💰 مبلغ: ' + order.amount + '\n📦 وضعیت: ' + order.statusText + '\n\n🛒 محصولات:\n' + (order.items ? order.items.join('\n') : '-')); }
function renderNotifications() { var container = document.getElementById('notifications-container'); var notifications = getStorage(STORAGE_KEYS.NOTIFICATIONS, DEFAULT_NOTIFICATIONS); var empty = document.getElementById('notifications-empty'); if (notifications.length === 0) { empty.style.display = 'block'; container.innerHTML = ''; return; } empty.style.display = 'none'; container.innerHTML = notifications.map(function(n, idx) { return '<div class="notification-item ' + (n.read ? '' : 'unread') + '" style="padding:15px;background:var(--bg-light);border-radius:8px;margin-bottom:10px;cursor:pointer" onclick="markNotifRead(' + idx + ')"><div style="display:flex;justify-content:space-between;align-items:flex-start"><strong style="font-size:15px">' + escapeHtml(n.title) + '</strong><span style="font-size:11px;color:var(--text-light);white-space:nowrap">' + escapeHtml(n.date) + '</span></div><p style="font-size:13px;color:var(--text-light);margin-top:6px;line-height:1.6">' + escapeHtml(n.body) + '</p>' + (!n.read ? '<span style="display:inline-block;width:8px;height:8px;background:var(--primary);border-radius:50%;margin-top:8px"></span>' : '') + '</div>'; }).join(''); }
function markNotifRead(idx) { var notifications = getStorage(STORAGE_KEYS.NOTIFICATIONS, DEFAULT_NOTIFICATIONS); if (notifications[idx]) { notifications[idx].read = true; setStorage(STORAGE_KEYS.NOTIFICATIONS, notifications); renderNotifications(); } }
function showProfileTab(tab) { document.querySelectorAll('.profile-tab').forEach(function(t) { t.style.display = 'none'; }); var el = document.getElementById('tab-' + tab); if (el) el.style.display = 'block'; document.querySelectorAll('.profile-menu a[data-tab]').forEach(function(a) { a.classList.remove('active'); }); var activeLink = document.querySelector('.profile-menu a[data-tab="' + tab + '"]'); if (activeLink) activeLink.classList.add('active'); if (tab === 'info') renderProfileInfo(); if (tab === 'addresses') renderAddresses(); if (tab === 'orders') renderOrders(); if (tab === 'notifications') renderNotifications(); window.location.hash = tab; }
function handleHash() { var hash = window.location.hash.replace('#', ''); if (hash && ['info', 'addresses', 'orders', 'notifications'].indexOf(hash) !== -1) { showProfileTab(hash); } }
window.addEventListener('hashchange', handleHash);
document.addEventListener('DOMContentLoaded', function() { if (!checkAuth()) return; renderSidebar(); renderProfileInfo(); handleHash(); });
</script>
</body>
</html>"""

def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ {path} ({len(content)} chars)")

def main():
    base = 'dotwatch-fixed-2'
    print("=" * 60)
    print("در حال ذخیره فایل‌ها...")
    print("=" * 60)

    save_file(os.path.join(base, 'js', 'auth.js'), AUTH_JS)
    save_file(os.path.join(base, 'login', 'index.html'), LOGIN_HTML)
    save_file(os.path.join(base, 'register', 'index.html'), REGISTER_HTML)
    save_file(os.path.join(base, 'profile', 'index.html'), PROFILE_HTML)

    print("\n" + "=" * 60)
    print("✅ همه فایل‌ها با موفقیت ذخیره شدند!")
    print("=" * 60)
    print("""
🔧 باگ‌های رفع شده:
  • auth.js: وقتی لاگین نیستی، هم «ورود» هم «ثبت نام» نشون داده می‌شه
  • auth.js: رمز عبور هم ذخیره می‌شه (قبلاً نمی‌شد)
  • login: رمز عبور چک می‌شه + سازگاری با کاربران قدیمی
  • register: تکرار رمز اضافه شد + رمز ذخیره می‌شه
  • profile: همه چی از dotwatch_user می‌خونه (نام، شماره، ایمیل...)
  • profile: تب‌ها داینامیک هستن + آدرس/سفارش/اعلان قابل مدیریت

⚠️  نکته مهم:
  اگه قبلاً ثبت‌نام کردی و رمز نداری، اولین ورود رمزت رو ثبت می‌کنه.
  برای تست تمیز، DevTools → Application → LocalStorage رو پاک کن.

🚀 نحوه تست:
  1. صفحه register/index.html → ثبت‌نام با شماره و رمز
  2. صفحه login/index.html → ورود با همون شماره و رمز
  3. صفحه profile/index.html → باید نام و شماره‌ات رو نشون بده
  4. خروج → دوباره ورود → باید کار کنه
""")

if __name__ == '__main__':
    main()
