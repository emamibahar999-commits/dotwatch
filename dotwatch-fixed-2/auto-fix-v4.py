#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DotWatch Auto-Fix v4
- Personal info populated from user input data
- Email is now OPTIONAL
- Phone number is REQUIRED
- Run: python3 auto-fix-v4.py
"""

import os
import re

# ===================== CLEAN AUTH.JS =====================
AUTH_JS = r"""// ==================== DOTWATCH USER AUTH v4 =======================
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

  login: function(userData) {
    var user = {
      id: userData.id || Date.now(),
      name: userData.name || 'کاربر',
      email: userData.email || '',
      phone: userData.phone || '',
      birthdate: userData.birthdate || '',
      avatar: userData.avatar || this.generateAvatar(userData.name || 'کاربر'),
      role: userData.role || 'user',
      createdAt: userData.createdAt || new Date().toISOString()
    };
    localStorage.setItem('dotwatch_user', JSON.stringify(user));
    this.renderUserAccount();
    if (typeof showNotification === 'function') {
      showNotification('خوش آمدید ' + user.name + ' 👋');
    }
    return user;
  },

  logout: function() {
    localStorage.removeItem('dotwatch_user');
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
          '<a href="' + prefix + 'orders/index.html" class="user-dropdown-item">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>' +
            '<span>سفارش‌های من</span>' +
          '</a>' +
          '<a href="' + prefix + 'addresses/index.html" class="user-dropdown-item">' +
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
      c.innerHTML = '<a href="' + prefix + 'register/index.html" class="action-btn">' +
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
"""

# ===================== REGISTER PAGE (phone required, email optional) =====================
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
    .form-group input, .form-group select {
      width: 100%; padding: 14px 16px; border: 1px solid #e5e0d8; border-radius: 12px;
      font-size: 14px; font-family: inherit; transition: all 0.3s; background: #fdfcfa;
    }
    .form-group input:focus, .form-group select:focus { outline: none; border-color: #c9a96e; background: #fff; box-shadow: 0 0 0 3px rgba(201,169,110,0.1); }
    .form-group input.error, .form-group select.error { border-color: #e74c3c; }
    .bd-row { display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 10px; }
    .err { color: #e74c3c; font-size: 12px; margin-top: 6px; display: none; }
    .err.show { display: block; }
    .btn-submit {
      width: 100%; padding: 15px; border: none; border-radius: 12px;
      background: linear-gradient(135deg, #c9a96e, #a08050); color: #fff;
      font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer;
      transition: all 0.3s; margin-top: 6px;
    }
    .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(201,169,110,0.35); }
    .auth-foot { text-align: center; margin-top: 28px; padding-top: 24px; border-top: 1px solid #f0ebe3; font-size: 14px; color: #777; }
    .auth-foot a { color: #c9a96e; text-decoration: none; font-weight: 600; }
    .auth-foot a:hover { text-decoration: underline; }
  </style>
</head>
<body>

<div class="top-bar"><div class="container">🎁 ارسال رایگان برای خرید بالای ۷۵ میلیون تومان | <a href="../discounts/index.html">مشاهده تخفیف‌ها</a></div></div>

<header class="header">
  <div class="container">
    <div class="header-main">
      <a href="../index.html" class="logo"><div class="logo-icon">⌚</div><span>دات واچ</span></a>
      <div class="search-box">
        <input type="text" id="search-input" placeholder="جستجوی ساعت، برند، مدل...">
        <button onclick="const v=document.getElementById('search-input').value;if(v)window.location.href='../watch/index.html?q='+encodeURIComponent(v)">🔍</button>
      </div>
      <div class="header-actions">
        <a href="../cart/index.html" class="action-btn">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>
          <span>سبد خرید</span>
        </a>
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

    <form id="register-form" novalidate>
      <div class="form-group">
        <label>نام و نام خانوادگی <span class="req">*</span></label>
        <input type="text" id="reg-name" placeholder="مثال: علی احمدی" required>
        <div class="err" id="err-name">لطفاً نام خود را وارد کنید</div>
      </div>

      <div class="form-group">
        <label>ایمیل <span class="opt">(اختیاری)</span></label>
        <input type="email" id="reg-email" placeholder="example@email.com">
      </div>

      <div class="form-group">
        <label>شماره موبایل <span class="req">*</span></label>
        <input type="tel" id="reg-phone" placeholder="0912xxxxxxx" required>
        <div class="err" id="err-phone">لطفاً شماره موبایل معتبر وارد کنید</div>
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
        <div class="err" id="err-birthdate">لطفاً تاریخ تولد کامل وارد کنید</div>
      </div>

      <div class="form-group">
        <label>رمز عبور <span class="req">*</span></label>
        <input type="password" id="reg-password" placeholder="حداقل ۶ کاراکتر" required minlength="6">
        <div class="err" id="err-password">رمز عبور باید حداقل ۶ کاراکتر باشد</div>
      </div>

      <button type="submit" class="btn-submit">ثبت نام</button>
    </form>

    <div class="auth-foot">
      قبلاً ثبت نام کردید؟ <a href="./login.html">ورود به حساب</a>
    </div>
  </div>
</main>

<footer class="footer" style="background:#1a1a1a;color:#fff;padding:50px 0 20px;margin-top:0">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:40px;margin-bottom:40px">
      <div>
        <h4 style="color:#c9a96e;margin-bottom:20px;font-size:18px">دات واچ</h4>
        <p style="color:#aaa;font-size:14px;line-height:1.8">فروشگاه تخصصی ساعت‌های مچی و اکسسوری با بهترین برندهای جهانی</p>
      </div>
      <div>
        <h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">دسترسی سریع</h4>
        <ul style="list-style:none;padding:0">
          <li style="margin-bottom:10px"><a href="../watch/index.html" style="color:#aaa;text-decoration:none;font-size:14px">ساعت مچی</a></li>
          <li style="margin-bottom:10px"><a href="../brands/index.html" style="color:#aaa;text-decoration:none;font-size:14px">برندها</a></li>
          <li style="margin-bottom:10px"><a href="../discounts/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تخفیفات</a></li>
        </ul>
      </div>
      <div>
        <h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">پشتیبانی</h4>
        <ul style="list-style:none;padding:0">
          <li style="margin-bottom:10px"><a href="../faq/index.html" style="color:#aaa;text-decoration:none;font-size:14px">سوالات متداول</a></li>
          <li style="margin-bottom:10px"><a href="../rules/index.html" style="color:#aaa;text-decoration:none;font-size:14px">قوانین</a></li>
          <li style="margin-bottom:10px"><a href="../contact/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تماس با ما</a></li>
        </ul>
      </div>
    </div>
    <div style="border-top:1px solid #333;padding-top:20px;text-align:center;color:#777;font-size:13px">
      © ۲۰۲۵ دات واچ. تمامی حقوق محفوظ است.
    </div>
  </div>
</footer>

<script src="../js/auth.js"></script>
<script>
  var dSel = document.getElementById('reg-day');
  for (var i = 1; i <= 31; i++) {
    var o = document.createElement('option');
    o.value = String(i).padStart(2, '0');
    o.textContent = i;
    dSel.appendChild(o);
  }
  var ySel = document.getElementById('reg-year');
  var cy = new Date().getFullYear();
  for (var i = cy - 18; i >= cy - 80; i--) {
    var o = document.createElement('option');
    o.value = i;
    o.textContent = i;
    ySel.appendChild(o);
  }

  function validatePhone(phone) {
    var p = phone.replace(/\D/g, '');
    return p.length === 11 && p.charAt(0) === '0';
  }

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

    document.querySelectorAll('.err').forEach(function(el) { el.classList.remove('show'); });
    document.querySelectorAll('input, select').forEach(function(el) { el.classList.remove('error'); });

    if (!name) {
      document.getElementById('err-name').classList.add('show');
      document.getElementById('reg-name').classList.add('error');
      ok = false;
    }
    if (!validatePhone(phone)) {
      document.getElementById('err-phone').classList.add('show');
      document.getElementById('reg-phone').classList.add('error');
      ok = false;
    }
    if (!day || !month || !year) {
      document.getElementById('err-birthdate').classList.add('show');
      document.querySelectorAll('.bd-row select').forEach(function(el) { el.classList.add('error'); });
      ok = false;
    }
    if (!pass || pass.length < 6) {
      document.getElementById('err-password').classList.add('show');
      document.getElementById('reg-password').classList.add('error');
      ok = false;
    }
    if (!ok) return;

    UserAuth.login({
      name: name,
      email: email,
      phone: phone,
      birthdate: year + '-' + month + '-' + day
    });
    setTimeout(function() { window.location.href = '../index.html'; }, 800);
  });
</script>
</body>
</html>
"""

# ===================== LOGIN PAGE =====================
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
    .form-group input {
      width: 100%; padding: 14px 16px; border: 1px solid #e5e0d8; border-radius: 12px;
      font-size: 14px; font-family: inherit; transition: all 0.3s; background: #fdfcfa;
    }
    .form-group input:focus { outline: none; border-color: #c9a96e; background: #fff; box-shadow: 0 0 0 3px rgba(201,169,110,0.1); }
    .btn-submit {
      width: 100%; padding: 15px; border: none; border-radius: 12px;
      background: linear-gradient(135deg, #c9a96e, #a08050); color: #fff;
      font-size: 15px; font-weight: 700; font-family: inherit; cursor: pointer;
      transition: all 0.3s; margin-top: 6px;
    }
    .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(201,169,110,0.35); }
    .auth-error { color: #e74c3c; font-size: 13px; text-align: center; margin-bottom: 16px; display: none; }
    .auth-error.show { display: block; }
    .auth-foot { text-align: center; margin-top: 28px; padding-top: 24px; border-top: 1px solid #f0ebe3; font-size: 14px; color: #777; }
    .auth-foot a { color: #c9a96e; text-decoration: none; font-weight: 600; }
    .auth-foot a:hover { text-decoration: underline; }
  </style>
</head>
<body>

<div class="top-bar"><div class="container">🎁 ارسال رایگان برای خرید بالای ۷۵ میلیون تومان | <a href="../discounts/index.html">مشاهده تخفیف‌ها</a></div></div>

<header class="header">
  <div class="container">
    <div class="header-main">
      <a href="../index.html" class="logo"><div class="logo-icon">⌚</div><span>دات واچ</span></a>
      <div class="search-box">
        <input type="text" id="search-input" placeholder="جستجوی ساعت، برند، مدل...">
        <button onclick="const v=document.getElementById('search-input').value;if(v)window.location.href='../watch/index.html?q='+encodeURIComponent(v)">🔍</button>
      </div>
      <div class="header-actions">
        <a href="../cart/index.html" class="action-btn">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>
          <span>سبد خرید</span>
        </a>
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

    <form id="login-form">
      <div class="form-group">
        <label>شماره موبایل یا ایمیل</label>
        <input type="text" id="login-id" placeholder="شماره موبایل یا ایمیل خود را وارد کنید" required>
      </div>
      <div class="form-group">
        <label>رمز عبور</label>
        <input type="password" id="login-password" placeholder="رمز عبور خود را وارد کنید" required>
      </div>
      <button type="submit" class="btn-submit">ورود</button>
    </form>

    <div class="auth-foot">
      حساب کاربری ندارید؟ <a href="./register.html">ثبت نام کنید</a>
    </div>
  </div>
</main>

<footer class="footer" style="background:#1a1a1a;color:#fff;padding:50px 0 20px;margin-top:0">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:40px;margin-bottom:40px">
      <div>
        <h4 style="color:#c9a96e;margin-bottom:20px;font-size:18px">دات واچ</h4>
        <p style="color:#aaa;font-size:14px;line-height:1.8">فروشگاه تخصصی ساعت‌های مچی و اکسسوری با بهترین برندهای جهانی</p>
      </div>
      <div>
        <h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">دسترسی سریع</h4>
        <ul style="list-style:none;padding:0">
          <li style="margin-bottom:10px"><a href="../watch/index.html" style="color:#aaa;text-decoration:none;font-size:14px">ساعت مچی</a></li>
          <li style="margin-bottom:10px"><a href="../brands/index.html" style="color:#aaa;text-decoration:none;font-size:14px">برندها</a></li>
          <li style="margin-bottom:10px"><a href="../discounts/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تخفیفات</a></li>
        </ul>
      </div>
      <div>
        <h4 style="color:#c9a96e;margin-bottom:20px;font-size:16px">پشتیبانی</h4>
        <ul style="list-style:none;padding:0">
          <li style="margin-bottom:10px"><a href="../faq/index.html" style="color:#aaa;text-decoration:none;font-size:14px">سوالات متداول</a></li>
          <li style="margin-bottom:10px"><a href="../rules/index.html" style="color:#aaa;text-decoration:none;font-size:14px">قوانین</a></li>
          <li style="margin-bottom:10px"><a href="../contact/index.html" style="color:#aaa;text-decoration:none;font-size:14px">تماس با ما</a></li>
        </ul>
      </div>
    </div>
    <div style="border-top:1px solid #333;padding-top:20px;text-align:center;color:#777;font-size:13px">
      © ۲۰۲۵ دات واچ. تمامی حقوق محفوظ است.
    </div>
  </div>
</footer>

<script src="../js/auth.js"></script>
<script>
  document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var id = document.getElementById('login-id').value.trim();
    var pass = document.getElementById('login-password').value;
    var err = document.getElementById('login-error');
    var user = UserAuth.getUser();
    if (user && (user.phone === id || user.email === id)) {
      UserAuth.login(user);
      setTimeout(function() { window.location.href = '../index.html'; }, 500);
    } else {
      err.classList.add('show');
    }
  });
</script>
</body>
</html>
"""

# ===================== CSS APPEND =====================
CSS_APPEND = """
/* === USER ACCOUNT DROPDOWN v4 === */
.user-account-wrapper{position:relative;display:inline-block}
.user-account-btn{display:flex;align-items:center;gap:8px;padding:6px 14px;border:1px solid #e0e0e0;border-radius:50px;background:#fff;cursor:pointer;transition:all .3s;font-family:inherit;color:#333;font-size:13px}
.user-account-btn:hover{border-color:#c9a96e;box-shadow:0 2px 12px rgba(0,0,0,.08)}
.user-avatar{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}
.user-name{font-size:13px;font-weight:500;white-space:nowrap;max-width:110px;overflow:hidden;text-overflow:ellipsis}
.user-dropdown-menu{position:absolute;top:calc(100% + 12px);right:0;min-width:280px;background:#fff;border-radius:16px;box-shadow:0 12px 48px rgba(0,0,0,.18);padding:10px 0;opacity:0;visibility:hidden;transform:translateY(-8px);transition:all .25s cubic-bezier(.4,0,.2,1);z-index:99999;border:1px solid rgba(0,0,0,.06);pointer-events:none}
.user-dropdown-menu.show{opacity:1;visibility:visible;transform:translateY(0);pointer-events:auto}
.user-dropdown-menu::before{content:"";position:absolute;top:-6px;right:28px;width:12px;height:12px;background:#fff;transform:rotate(45deg);border-top:1px solid rgba(0,0,0,.06);border-right:1px solid rgba(0,0,0,.06)}
.user-dropdown-header{display:flex;align-items:center;gap:12px;padding:18px 22px 14px}
.user-avatar-large{width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:700;flex-shrink:0}
.user-info{display:flex;flex-direction:column;gap:3px;overflow:hidden;direction:rtl;text-align:right}
.user-name-large{font-size:15px;font-weight:600;color:#333;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.user-detail-row{font-size:12px;color:#888;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:6px}
.user-detail-row svg{width:14px;height:14px;opacity:.6;flex-shrink:0}
.user-dropdown-divider{height:1px;background:linear-gradient(to right,transparent,#e8e8e8,transparent);margin:6px 18px}
.user-dropdown-item{display:flex;align-items:center;gap:12px;padding:12px 22px;color:#444;text-decoration:none;font-size:14px;transition:all .15s;cursor:pointer;background:none;border:none;width:100%;font-family:inherit;text-align:right;direction:rtl}
.user-dropdown-item:hover{background:rgba(201,169,110,.08);color:#c9a96e}
.user-dropdown-item svg{flex-shrink:0;opacity:.65}
.user-dropdown-item:hover svg{opacity:1}
.user-logout-btn{color:#e74c3c}
.user-logout-btn:hover{background:rgba(231,76,60,.08);color:#e74c3c}
@media(max-width:768px){.user-name{display:none}.user-account-btn{padding:6px}.user-dropdown-menu{min-width:240px}}
"""

def find_html_files(root_dir):
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules','venv','__pycache__']]
        for fname in filenames:
            if fname.endswith('.html'):
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)

def get_relative_prefix(filepath, root_dir):
    rel = os.path.relpath(filepath, root_dir)
    depth = rel.count(os.sep)
    if depth == 0:
        return './'
    return '../' * depth

def fix_header_actions(content):
    content = re.sub(r'<a\s+href="[^"]*compare[^"]*"\s+class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*مقایسه\s*</span>\s*</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a\s+href="[^"]*wishlist[^"]*"\s+class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*علاقه[\s‌]*مندی[\s‌]*ها\s*</span>\s*</a>', '', content, flags=re.DOTALL)
    return content

def replace_login_with_container(content):
    pattern = r'<a\s+href="[^"]*login/index\.html"\s+class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*حساب کاربری\s*</span>\s*</a>'
    replacement = '<div id="user-account-container"></div>'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if new_content == content:
        pattern2 = r'<a\s+[^>]*class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*حساب کاربری\s*</span>\s*</a>'
        new_content = re.sub(pattern2, replacement, content, count=1, flags=re.DOTALL)
    return new_content

def add_auth_script(content, prefix):
    if 'auth.js' in content:
        return content
    script_tag = f'  <!-- User Auth -->\n  <script src="{prefix}js/auth.js"></script>\n</body>'
    if '</body>' in content:
        content = content.replace('</body>', script_tag, 1)
    else:
        content += f'\n<script src="{prefix}js/auth.js"></script>\n'
    return content

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    print("=" * 60)
    print("   DotWatch Auto-Fix v4")
    print("=" * 60)
    print(f"\nProject root: {root}\n")

    js_dir = os.path.join(root, 'js')
    os.makedirs(js_dir, exist_ok=True)
    with open(os.path.join(js_dir, 'auth.js'), 'w', encoding='utf-8') as f:
        f.write(AUTH_JS)
    print("✅ js/auth.js  (personal info from input data)")

    css_path = os.path.join(root, 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            existing = f.read()
        if 'user-account-wrapper' not in existing:
            with open(css_path, 'a', encoding='utf-8') as f:
                f.write(CSS_APPEND)
            print("✅ css/style.css  (styles added)")
        else:
            print("⏭️  css/style.css  (already has styles)")
    else:
        print("⚠️  css/style.css not found")

    reg_dir = os.path.join(root, 'register')
    os.makedirs(reg_dir, exist_ok=True)
    with open(os.path.join(reg_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(REGISTER_HTML)
    print("✅ register/index.html  (phone required, email optional)")

    login_dir = os.path.join(root, 'login')
    os.makedirs(login_dir, exist_ok=True)
    with open(os.path.join(login_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(LOGIN_HTML)
    print("✅ login/index.html  (login with phone or email)")

    html_files = find_html_files(root)
    print(f"\n🔍 Found {len(html_files)} HTML file(s)\n")

    modified = 0
    for filepath in html_files:
        rel = os.path.relpath(filepath, root)
        if 'register/index.html' in rel.replace('\\', '/') or 'login/index.html' in rel.replace('\\', '/'):
            print(f"  ⏭️  Skipped  →  {rel}")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content
        prefix = get_relative_prefix(filepath, root)

        content = fix_header_actions(content)
        content = replace_login_with_container(content)
        content = add_auth_script(content, prefix)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Modified  →  {rel}")
            modified += 1
        else:
            print(f"  ⏭️  Skipped  →  {rel}")

    print(f"\n{'=' * 60}")
    print(f"Done! {modified} HTML file(s) modified.")
    print(f"{'=' * 60}")
    print("""
What's new in v4:
  ✅ Personal info in dropdown populated from user input data
  ✅ Email is now OPTIONAL in registration
  ✅ Phone number is REQUIRED in registration
  ✅ Phone validation (11 digits, starts with 0)
  ✅ Login works with phone OR email
  ✅ Register/Login pages use main site template
  ✅ Compare & Wishlist removed from all headers
""")

if __name__ == '__main__':
    main()
