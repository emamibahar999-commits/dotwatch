const ADMIN_API = window.API || {};

async function loadAdminData() {
  try {
    const data = await ADMIN_API.Admin.getData();
    if (data.products) window.adminProducts = data.products;
    if (data.orders) window.adminOrders = data.orders;
    if (data.users) window.adminUsers = data.users;
    if (data.banners) window.adminBanners = data.banners;
    if (data.settings) window.adminSettings = data.settings;
    console.log('Admin data loaded from API');
    if (typeof renderDashboard === 'function') renderDashboard();
    if (typeof renderProducts === 'function') renderProducts();
    if (typeof renderOrders === 'function') renderOrders();
    if (typeof renderUsers === 'function') renderUsers();
  } catch(e) { console.log('Using localStorage (API unavailable)'); }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadAdminData);
} else { loadAdminData(); }
