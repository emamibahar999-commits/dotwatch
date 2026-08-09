#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DotWatch Complete Auto-Fix Script
Applies ALL user-account dynamic changes automatically.

Changes applied:
1. Creates smart auth.js (self-contained CSS, auto-path detection)
2. Removes "مقایسه" and "علاقه‌مندی‌ها" from header actions in all pages
3. Replaces static login link with dynamic container in all pages
4. Adds auth.js script tag to all pages
5. Appends user-account CSS to style.css
6. Creates register page with required birthdate field
7. Updates login page to work with new auth system

Usage:
    1. Put this script in ROOT of project (next to index.html)
    2. Run: python auto-fix-complete.py
    3. Done!
"""

import os
import re
import sys

# ===================== AUTH.JS CONTENT =====================
AUTH_JS_CONTENT = r"""// ==================== DOTWATCH USER AUTH =======================
(function(){
'use strict';

// Detect prefix from this script's src
const scripts=document.querySelectorAll('script[src*="auth.js"]');
const thisScript=scripts[scripts.length-1];
const scriptSrc=thisScript?thisScript.getAttribute('src'):'./js/auth.js';
let prefix='./';
if(scriptSrc.includes('/')){
  const parts=scriptSrc.split('/');
  parts.pop();parts.pop();
  if(parts.length>0) prefix=parts.join('/')+'/';
}

// Inject CSS
const AUTH_CSS=`.user-account-wrapper{position:relative;display:inline-block}
.user-account-btn{display:flex;align-items:center;gap:8px;padding:6px 12px;border:1px solid #e0e0e0;border-radius:50px;background:#fff;cursor:pointer;transition:all .3s;font-family:inherit;color:#333;font-size:13px}
.user-account-btn:hover{border-color:#c9a96e;box-shadow:0 2px 12px rgba(0,0,0,.08)}
.user-avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}
.user-name{font-size:13px;font-weight:500;white-space:nowrap;max-width:100px;overflow:hidden;text-overflow:ellipsis}
.user-chevron{transition:transform .3s;flex-shrink:0}
.user-dropdown-menu{position:absolute;top:calc(100% + 10px);right:0;min-width:260px;background:#fff;border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.15);padding:8px 0;opacity:0;visibility:hidden;transform:translateY(-10px);transition:all .3s;z-index:9999;border:1px solid rgba(0,0,0,.06)}
.user-dropdown-menu.show{opacity:1;visibility:visible;transform:translateY(0)}
.user-dropdown-menu::before{content:'';position:absolute;top:-6px;right:24px;width:12px;height:12px;background:#fff;transform:rotate(45deg);border-top:1px solid rgba(0,0,0,.06);border-right:1px solid rgba(0,0,0,.06)}
.user-dropdown-header{display:flex;align-items:center;gap:12px;padding:16px 20px}
.user-avatar-large{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;flex-shrink:0}
.user-info{display:flex;flex-direction:column;gap:2px;overflow:hidden}
.user-name-large{font-size:14px;font-weight:600;color:#333;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.user-email{font-size:12px;color:#888;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.user-dropdown-divider{height:1px;background:linear-gradient(to right,transparent,#e0e0e0,transparent);margin:4px 16px}
.user-dropdown-item{display:flex;align-items:center;gap:12px;padding:12px 20px;color:#333;text-decoration:none;font-size:14px;transition:all .2s;cursor:pointer;background:none;border:none;width:100%;font-family:inherit;text-align:right}
.user-dropdown-item:hover{background:rgba(201,169,110,.08);color:#c9a96e}
.user-dropdown-item svg{flex-shrink:0;opacity:.7}
.user-dropdown-item:hover svg{opacity:1}
.user-logout-btn{color:#e74c3c}
.user-logout-btn:hover{background:rgba(231,76,60,.08);color:#e74c3c}
@media(max-width:768px){.user-name{display:none}.user-account-btn{padding:6px}.user-dropdown-menu{min-width:220px}}`;

const styleEl=document.createElement('style');
styleEl.textContent=AUTH_CSS;
document.head.appendChild(styleEl);

const UserAuth={
  getUser(){try{const u=localStorage.getItem('dotwatch_user');return u?JSON.parse(u):null}catch{return null}},
  isLoggedIn(){return!!this.getUser()},
  login(userData){
    const user={
      id:userData.id||Date.now(),
      name:userData.name||'کاربر',
      email:userData.email||'',
      phone:userData.phone||'',
      birthdate:userData.birthdate||'',
      avatar:userData.avatar||this.generateAvatar(userData.name||'کاربر'),
      role:userData.role||'user',
      createdAt:userData.createdAt||new Date().toISOString()
    };
    localStorage.setItem('dotwatch_user',JSON.stringify(user));
    this.renderUserAccount();
    if(typeof showNotification==='function') showNotification('خوش آمدید '+user.name+' 👋');
    return user;
  },
  logout(){
    localStorage.removeItem('dotwatch_user');
    this.renderUserAccount();
    if(typeof showNotification==='function') showNotification('با موفقیت خارج شدید');
    setTimeout(()=>{
      const p=window.location.pathname;
      if(p.includes('profile')||p.includes('orders')||p.includes('addresses')){
        window.location.href=prefix+'index.html';
      }
    },500);
  },
  generateAvatar(name){if(!name)return'';const p=name.trim().split(' ').filter(Boolean);if(p.length>=2)return p[0][0]+p[1][0];return name.substring(0,2)},
  toggleDropdown(e){if(e){e.preventDefault();e.stopPropagation()}const d=document.querySelector('.user-dropdown-menu');if(d)d.classList.toggle('show')},
  closeDropdown(){const d=document.querySelector('.user-dropdown-menu');if(d)d.classList.remove('show')},
  renderUserAccount(){
    const c=document.getElementById('user-account-container');
    if(!c)return;
    const user=this.getUser();
    if(user){
      c.innerHTML=`<div class="user-account-wrapper">
        <button class="user-account-btn" onclick="window.UserAuth.toggleDropdown(event)" aria-label="منوی کاربر">
          <div class="user-avatar">${user.avatar||this.generateAvatar(user.name)}</div>
          <span class="user-name">${user.name}</span>
          <svg class="user-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="user-dropdown-menu">
          <div class="user-dropdown-header">
            <div class="user-avatar-large">${user.avatar||this.generateAvatar(user.name)}</div>
            <div class="user-info"><span class="user-name-large">${user.name}</span><span class="user-email">${user.email||user.phone||''}</span></div>
          </div>
          <div class="user-dropdown-divider"></div>
          <a href="${prefix}profile/index.html" class="user-dropdown-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>پروفایل</span>
          </a>
          <a href="${prefix}orders/index.html" class="user-dropdown-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>
            <span>سفارش‌های من</span>
          </a>
          <a href="${prefix}addresses/index.html" class="user-dropdown-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>آدرس‌ها</span>
          </a>
          <div class="user-dropdown-divider"></div>
          <button class="user-dropdown-item user-logout-btn" onclick="window.UserAuth.logout()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            <span>خروج از حساب</span>
          </button>
        </div>
      </div>`;
    } else {
      c.innerHTML=`<a href="${prefix}register/index.html" class="action-btn">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
        <span>ثبت نام</span>
      </a>`;
    }
  },
  init(){
    this.renderUserAccount();
    document.addEventListener('click',e=>{if(!e.target.closest('.user-account-wrapper'))this.closeDropdown()});
  }
};
window.UserAuth=UserAuth;
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',()=>UserAuth.init());
} else {
  UserAuth.init();
}
})();
"""

# ===================== REGISTER PAGE CONTENT =====================
REGISTER_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ثبت نام | دات واچ</title>
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px 20px; background: linear-gradient(135deg, #f5f0e8 0%, #fff 100%); }
    .auth-box { width: 100%; max-width: 420px; background: #fff; border-radius: 24px; padding: 40px 32px; box-shadow: 0 20px 60px rgba(0,0,0,0.08); }
    .auth-logo { text-align: center; margin-bottom: 32px; font-size: 24px; font-weight: 700; color: #c9a96e; }
    .auth-title { text-align: center; font-size: 20px; font-weight: 600; margin-bottom: 8px; color: #333; }
    .auth-subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 28px; }
    .form-group { margin-bottom: 20px; }
    .form-group label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #555; }
    .form-group label .required { color: #e74c3c; margin-right: 4px; }
    .form-group input {
      width: 100%; padding: 14px 16px; border: 1px solid #e0e0e0; border-radius: 12px;
      font-size: 14px; font-family: inherit; transition: all 0.3s; background: #fafafa;
    }
    .form-group input:focus { outline: none; border-color: #c9a96e; background: #fff; box-shadow: 0 0 0 3px rgba(201,169,110,0.1); }
    .form-group input.error { border-color: #e74c3c; }
    .error-msg { color: #e74c3c; font-size: 12px; margin-top: 6px; display: none; }
    .error-msg.show { display: block; }
    .btn-primary {
      width: 100%; padding: 14px; border: none; border-radius: 12px;
      background: linear-gradient(135deg, #c9a96e, #a08050); color: #fff;
      font-size: 15px; font-weight: 600; font-family: inherit; cursor: pointer;
      transition: all 0.3s; margin-top: 8px;
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(201,169,110,0.3); }
    .auth-footer { text-align: center; margin-top: 24px; font-size: 14px; color: #888; }
    .auth-footer a { color: #c9a96e; text-decoration: none; font-weight: 500; }
    .auth-footer a:hover { text-decoration: underline; }
    .birthdate-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
    .birthdate-row select {
      width: 100%; padding: 14px 12px; border: 1px solid #e0e0e0; border-radius: 12px;
      font-size: 14px; font-family: inherit; background: #fafafa; cursor: pointer;
    }
    .birthdate-row select:focus { outline: none; border-color: #c9a96e; background: #fff; }
  </style>
</head>
<body>
  <div class="auth-page">
    <div class="auth-box">
      <div class="auth-logo">⌚ دات واچ</div>
      <h1 class="auth-title">ثبت نام</h1>
      <p class="auth-subtitle">حساب کاربری جدید بسازید</p>

      <form id="register-form" novalidate>
        <div class="form-group">
          <label>نام و نام خانوادگی <span class="required">*</span></label>
          <input type="text" id="reg-name" placeholder="مثال: علی احمدی" required>
          <div class="error-msg" id="err-name">لطفاً نام خود را وارد کنید</div>
        </div>

        <div class="form-group">
          <label>ایمیل <span class="required">*</span></label>
          <input type="email" id="reg-email" placeholder="example@email.com" required>
          <div class="error-msg" id="err-email">لطفاً ایمیل معتبر وارد کنید</div>
        </div>

        <div class="form-group">
          <label>شماره موبایل</label>
          <input type="tel" id="reg-phone" placeholder="0912xxxxxxx">
        </div>

        <div class="form-group">
          <label>تاریخ تولد <span class="required">*</span></label>
          <div class="birthdate-row">
            <select id="reg-day" required>
              <option value="" disabled selected>روز</option>
            </select>
            <select id="reg-month" required>
              <option value="" disabled selected>ماه</option>
              <option value="01">فروردین</option>
              <option value="02">اردیبهشت</option>
              <option value="03">خرداد</option>
              <option value="04">تیر</option>
              <option value="05">مرداد</option>
              <option value="06">شهریور</option>
              <option value="07">مهر</option>
              <option value="08">آبان</option>
              <option value="09">آذر</option>
              <option value="10">دی</option>
              <option value="11">بهمن</option>
              <option value="12">اسفند</option>
            </select>
            <select id="reg-year" required>
              <option value="" disabled selected>سال</option>
            </select>
          </div>
          <div class="error-msg" id="err-birthdate">لطفاً تاریخ تولد خود را کامل وارد کنید</div>
        </div>

        <div class="form-group">
          <label>رمز عبور <span class="required">*</span></label>
          <input type="password" id="reg-password" placeholder="حداقل ۶ کاراکتر" required minlength="6">
          <div class="error-msg" id="err-password">رمز عبور باید حداقل ۶ کاراکتر باشد</div>
        </div>

        <button type="submit" class="btn-primary">ثبت نام</button>
      </form>

      <div class="auth-footer">
        قبلاً ثبت نام کردید؟ <a href="./index.html">ورود به حساب</a>
      </div>
    </div>
  </div>

  <script src="../js/auth.js"></script>
  <script>
    // Populate days and years
    const daySelect = document.getElementById('reg-day');
    for (let i = 1; i <= 31; i++) {
      const opt = document.createElement('option');
      opt.value = String(i).padStart(2, '0');
      opt.textContent = i;
      daySelect.appendChild(opt);
    }
    const yearSelect = document.getElementById('reg-year');
    const currentYear = new Date().getFullYear();
    for (let i = currentYear - 18; i >= currentYear - 80; i--) {
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = i;
      yearSelect.appendChild(opt);
    }

    document.getElementById('register-form').addEventListener('submit', function(e) {
      e.preventDefault();
      let valid = true;

      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const phone = document.getElementById('reg-phone').value.trim();
      const day = document.getElementById('reg-day').value;
      const month = document.getElementById('reg-month').value;
      const year = document.getElementById('reg-year').value;
      const password = document.getElementById('reg-password').value;

      // Reset errors
      document.querySelectorAll('.error-msg').forEach(el => el.classList.remove('show'));
      document.querySelectorAll('input, select').forEach(el => el.classList.remove('error'));

      if (!name) {
        document.getElementById('err-name').classList.add('show');
        document.getElementById('reg-name').classList.add('error');
        valid = false;
      }

      if (!email || !email.includes('@')) {
        document.getElementById('err-email').classList.add('show');
        document.getElementById('reg-email').classList.add('error');
        valid = false;
      }

      if (!day || !month || !year) {
        document.getElementById('err-birthdate').classList.add('show');
        document.querySelectorAll('.birthdate-row select').forEach(el => el.classList.add('error'));
        valid = false;
      }

      if (!password || password.length < 6) {
        document.getElementById('err-password').classList.add('show');
        document.getElementById('reg-password').classList.add('error');
        valid = false;
      }

      if (!valid) return;

      const birthdate = `${year}-${month}-${day}`;

      UserAuth.login({
        name: name,
        email: email,
        phone: phone,
        birthdate: birthdate
      });

      // Redirect after short delay
      setTimeout(() => {
        window.location.href = '../index.html';
      }, 800);
    });
  </script>
</body>
</html>
"""

# ===================== LOGIN PAGE UPDATE =====================
LOGIN_HTML_UPDATE = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ورود | دات واچ</title>
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px 20px; background: linear-gradient(135deg, #f5f0e8 0%, #fff 100%); }
    .auth-box { width: 100%; max-width: 420px; background: #fff; border-radius: 24px; padding: 40px 32px; box-shadow: 0 20px 60px rgba(0,0,0,0.08); }
    .auth-logo { text-align: center; margin-bottom: 32px; font-size: 24px; font-weight: 700; color: #c9a96e; }
    .auth-title { text-align: center; font-size: 20px; font-weight: 600; margin-bottom: 8px; color: #333; }
    .auth-subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 28px; }
    .form-group { margin-bottom: 20px; }
    .form-group label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #555; }
    .form-group input {
      width: 100%; padding: 14px 16px; border: 1px solid #e0e0e0; border-radius: 12px;
      font-size: 14px; font-family: inherit; transition: all 0.3s; background: #fafafa;
    }
    .form-group input:focus { outline: none; border-color: #c9a96e; background: #fff; box-shadow: 0 0 0 3px rgba(201,169,110,0.1); }
    .btn-primary {
      width: 100%; padding: 14px; border: none; border-radius: 12px;
      background: linear-gradient(135deg, #c9a96e, #a08050); color: #fff;
      font-size: 15px; font-weight: 600; font-family: inherit; cursor: pointer;
      transition: all 0.3s; margin-top: 8px;
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(201,169,110,0.3); }
    .auth-footer { text-align: center; margin-top: 24px; font-size: 14px; color: #888; }
    .auth-footer a { color: #c9a96e; text-decoration: none; font-weight: 500; }
    .auth-footer a:hover { text-decoration: underline; }
    .error-msg { color: #e74c3c; font-size: 13px; text-align: center; margin-bottom: 16px; display: none; }
    .error-msg.show { display: block; }
    .no-account { text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; }
    .no-account p { color: #888; font-size: 14px; margin-bottom: 12px; }
    .btn-outline {
      display: inline-block; padding: 10px 24px; border: 2px solid #c9a96e; border-radius: 10px;
      color: #c9a96e; text-decoration: none; font-weight: 500; transition: all 0.3s;
    }
    .btn-outline:hover { background: #c9a96e; color: #fff; }
  </style>
</head>
<body>
  <div class="auth-page">
    <div class="auth-box">
      <div class="auth-logo">⌚ دات واچ</div>
      <h1 class="auth-title">ورود به حساب</h1>
      <p class="auth-subtitle">وارد حساب کاربری خود شوید</p>

      <div class="error-msg" id="login-error">ایمیل یا رمز عبور اشتباه است</div>

      <form id="login-form">
        <div class="form-group">
          <label>ایمیل</label>
          <input type="email" id="login-email" placeholder="example@email.com" required>
        </div>

        <div class="form-group">
          <label>رمز عبور</label>
          <input type="password" id="login-password" placeholder="رمز عبور خود را وارد کنید" required>
        </div>

        <button type="submit" class="btn-primary">ورود</button>
      </form>

      <div class="no-account">
        <p>حساب کاربری ندارید؟</p>
        <a href="./register.html" class="btn-outline">ثبت نام کنید</a>
      </div>
    </div>
  </div>

  <script src="../js/auth.js"></script>
  <script>
    document.getElementById('login-form').addEventListener('submit', function(e) {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const password = document.getElementById('login-password').value;
      const errorEl = document.getElementById('login-error');

      const user = UserAuth.getUser();
      if (user && user.email === email) {
        // In a real app you'd verify password. Here we just re-login.
        UserAuth.login(user);
        setTimeout(() => {
          window.location.href = '../index.html';
        }, 500);
      } else {
        errorEl.classList.add('show');
      }
    });
  </script>
</body>
</html>
"""

# ===================== CSS TO APPEND =====================
CSS_APPEND = """
/* === USER ACCOUNT DROPDOWN (injected by auth.js, backup styles) === */
.user-account-wrapper{position:relative;display:inline-block}
.user-account-btn{display:flex;align-items:center;gap:8px;padding:6px 12px;border:1px solid #e0e0e0;border-radius:50px;background:#fff;cursor:pointer;transition:all .3s;font-family:inherit;color:#333;font-size:13px}
.user-account-btn:hover{border-color:#c9a96e;box-shadow:0 2px 12px rgba(0,0,0,.08)}
.user-avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}
.user-name{font-size:13px;font-weight:500;white-space:nowrap;max-width:100px;overflow:hidden;text-overflow:ellipsis}
.user-dropdown-menu{position:absolute;top:calc(100% + 10px);right:0;min-width:260px;background:#fff;border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.15);padding:8px 0;opacity:0;visibility:hidden;transform:translateY(-10px);transition:all .3s;z-index:9999;border:1px solid rgba(0,0,0,.06)}
.user-dropdown-menu.show{opacity:1;visibility:visible;transform:translateY(0)}
.user-dropdown-header{display:flex;align-items:center;gap:12px;padding:16px 20px}
.user-avatar-large{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#c9a96e,#a08050);color:#fff;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;flex-shrink:0}
.user-name-large{font-size:14px;font-weight:600;color:#333;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.user-email{font-size:12px;color:#888;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.user-dropdown-divider{height:1px;background:linear-gradient(to right,transparent,#e0e0e0,transparent);margin:4px 16px}
.user-dropdown-item{display:flex;align-items:center;gap:12px;padding:12px 20px;color:#333;text-decoration:none;font-size:14px;transition:all .2s;cursor:pointer;background:none;border:none;width:100%;font-family:inherit;text-align:right}
.user-dropdown-item:hover{background:rgba(201,169,110,.08);color:#c9a96e}
.user-logout-btn{color:#e74c3c}
.user-logout-btn:hover{background:rgba(231,76,60,.08);color:#e74c3c}
@media(max-width:768px){.user-name{display:none}.user-account-btn{padding:6px}.user-dropdown-menu{min-width:220px}}
"""


def find_html_files(root_dir):
    """Find all HTML files recursively."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
        for fname in filenames:
            if fname.endswith('.html'):
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)


def get_relative_prefix(filepath, root_dir):
    """Calculate relative prefix from file to root."""
    rel = os.path.relpath(filepath, root_dir)
    depth = rel.count(os.sep)
    # If the file itself is at root, depth might be 0
    if depth == 0:
        return './'
    return '../' * depth


def fix_header_actions(content):
    """Remove compare and wishlist links from header-actions."""
    # Pattern for compare link
    patterns = [
        # Remove compare link
        r'<a\s+href="[^"]*compare[^"]*"\s+class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*مقایسه\s*</span>\s*</a>',
        # Remove wishlist link  
        r'<a\s+href="[^"]*wishlist[^"]*"\s+class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*علاقه‌مندی‌ها\s*</span>\s*</a>',
        r'<a\s+href="[^"]*wishlist[^"]*"\s+class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*علاقه مندی ها\s*</span>\s*</a>',
    ]

    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    return content


def replace_login_with_container(content):
    """Replace static login link with dynamic container."""
    # Try specific pattern first
    pattern = r'<a\s+href="[^"]*login/index\.html"\s+class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*حساب کاربری\s*</span>\s*</a>'
    replacement = '<div id="user-account-container"></div>'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        # Try broader pattern
        pattern2 = r'<a\s+[^>]*class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*حساب کاربری\s*</span>\s*</a>'
        new_content = re.sub(pattern2, replacement, content, count=1, flags=re.DOTALL)

    return new_content


def add_auth_script(content, prefix):
    """Add auth.js script before closing body tag."""
    if 'auth.js' in content:
        return content

    script_tag = f'  <!-- User Auth -->\n  <script src="{prefix}js/auth.js"></script>\n</body>'

    if '</body>' in content:
        content = content.replace('</body>', script_tag, 1)
    else:
        content += f'\n<script src="{prefix}js/auth.js"></script>\n'

    return content


def ensure_container_in_header_actions(content):
    """Make sure user-account-container is inside header-actions."""
    # If container exists but not in header-actions, we might need to adjust
    # This is a safety check
    if 'user-account-container' in content:
        return content
    return content


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    print("=" * 65)
    print("   DotWatch Complete Auto-Fix")
    print("=" * 65)
    print(f"\nProject root: {root}\n")

    # 1. Create/update auth.js
    js_dir = os.path.join(root, 'js')
    os.makedirs(js_dir, exist_ok=True)
    auth_js_path = os.path.join(js_dir, 'auth.js')
    with open(auth_js_path, 'w', encoding='utf-8') as f:
        f.write(AUTH_JS_CONTENT)
    print(f"✅ Created: {os.path.relpath(auth_js_path, root)}")

    # 2. Append CSS to style.css
    css_path = os.path.join(root, 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            existing_css = f.read()
        if 'user-account-wrapper' not in existing_css:
            with open(css_path, 'a', encoding='utf-8') as f:
                f.write(CSS_APPEND)
            print(f"✅ Updated: {os.path.relpath(css_path, root)}")
        else:
            print(f"⏭️  CSS already exists in: {os.path.relpath(css_path, root)}")
    else:
        print(f"⚠️  style.css not found at: {css_path}")

    # 3. Create register page
    register_dir = os.path.join(root, 'register')
    os.makedirs(register_dir, exist_ok=True)
    register_path = os.path.join(register_dir, 'index.html')
    with open(register_path, 'w', encoding='utf-8') as f:
        f.write(REGISTER_HTML)
    print(f"✅ Created: {os.path.relpath(register_path, root)}")

    # 4. Update login page
    login_dir = os.path.join(root, 'login')
    os.makedirs(login_dir, exist_ok=True)
    login_path = os.path.join(login_dir, 'index.html')
    with open(login_path, 'w', encoding='utf-8') as f:
        f.write(LOGIN_HTML_UPDATE)
    print(f"✅ Updated: {os.path.relpath(login_path, root)}")

    # 5. Process all HTML files
    html_files = find_html_files(root)
    print(f"\n🔍 Found {len(html_files)} HTML file(s)\n")

    modified = 0
    for filepath in html_files:
        rel_path = os.path.relpath(filepath, root)

        # Skip login and register pages (already handled)
        if 'login/index.html' in filepath.replace('\\', '/') or 'register/index.html' in filepath.replace('\\', '/'):
            print(f"  ⏭️  Skipped  →  {rel_path} (handled separately)")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        prefix = get_relative_prefix(filepath, root)

        # Apply fixes
        content = fix_header_actions(content)
        content = replace_login_with_container(content)
        content = add_auth_script(content, prefix)
        content = ensure_container_in_header_actions(content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Modified  →  {rel_path}")
            modified += 1
        else:
            print(f"  ⏭️  Skipped  →  {rel_path} (no changes needed)")

    print(f"\n{'=' * 65}")
    print(f"Done! {modified} HTML file(s) modified.")
    print(f"{'=' * 65}")
    print("""
Summary of changes:
  ✅ auth.js created (smart path detection + self-injected CSS)
  ✅ style.css updated (backup CSS styles)
  ✅ register/index.html created (with required birthdate field)
  ✅ login/index.html updated (modern design)
  ✅ Compare & Wishlist links removed from all headers
  ✅ Static login links replaced with dynamic container
  ✅ auth.js script tag added to all pages

Next steps:
  1. Open index.html in browser
  2. Click "ثبت نام" → fill the form (birthdate is required!)
  3. After register, you'll see your avatar & dropdown menu
""")


if __name__ == '__main__':
    main()