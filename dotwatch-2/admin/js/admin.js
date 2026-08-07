/* Admin Panel JS */
const AdminState = {
    currentPage: 'dashboard',
    isLoggedIn: localStorage.getItem('admin_auth') === 'true'
};

function adminLogin(e) {
    e.preventDefault();
    const email = document.getElementById('admin-email').value;
    const pass = document.getElementById('admin-pass').value;
    if (email === 'admin@dotwatch.ir' && pass === 'admin123') {
        localStorage.setItem('admin_auth', 'true');
        location.href = 'index.html';
    } else {
        alert('ایمیل یا رمز عبور اشتباه است!');
    }
}

function adminLogout() {
    localStorage.removeItem('admin_auth');
    location.href = 'login.html';
}

function checkAuth() {
    if (!localStorage.getItem('admin_auth')) {
        location.href = 'login.html';
    }
}

function loadStats() {
    const stats = AdminAPI.getStats();
    document.getElementById('stat-products').textContent = stats.totalProducts;
    document.getElementById('stat-orders').textContent = stats.totalOrders;
    document.getElementById('stat-users').textContent = stats.totalUsers;
    document.getElementById('stat-revenue').textContent = (stats.totalRevenue / 1000000).toFixed(1) + 'M';
}

function renderProducts() {
    const tbody = document.getElementById('products-table');
    if (!tbody) return;
    tbody.innerHTML = AdminAPI.products.map(p => `
        <tr>
            <td>#${p.id}</td>
            <td><strong>${p.name}</strong></td>
            <td>${p.brand}</td>
            <td>${p.price.toLocaleString()} تومان</td>
            <td>${p.stock}</td>
            <td><span class="badge badge-${p.status === 'active' ? 'success' : 'danger'}">${p.status === 'active' ? 'فعال' : 'غیرفعال'}</span></td>
            <td>
                <div class="table-actions">
                    <button class="btn-edit" onclick="editProduct('${p.id}')" title="ویرایش"><i class="fas fa-edit"></i></button>
                    <button class="btn-delete" onclick="deleteProduct('${p.id}')" title="حذف"><i class="fas fa-trash"></i></button>
                </div>
            </td>
        </tr>
    `).join('');
}

function renderOrders() {
    const tbody = document.getElementById('orders-table');
    if (!tbody) return;
    tbody.innerHTML = AdminAPI.orders.map(o => `
        <tr>
            <td>${o.id}</td>
            <td>${o.customer}</td>
            <td>${o.total.toLocaleString()} تومان</td>
            <td><span class="badge badge-${o.status === 'delivered' ? 'success' : o.status === 'pending' ? 'warning' : 'info'}">${o.status === 'delivered' ? 'تحویل شده' : o.status === 'pending' ? 'در انتظار' : 'در حال پردازش'}</span></td>
            <td>${o.date}</td>
            <td>
                <div class="table-actions">
                    <button class="btn-edit" title="مشاهده"><i class="fas fa-eye"></i></button>
                </div>
            </td>
        </tr>
    `).join('');
}

function renderUsers() {
    const tbody = document.getElementById('users-table');
    if (!tbody) return;
    tbody.innerHTML = AdminAPI.users.map(u => `
        <tr>
            <td>#${u.id}</td>
            <td>${u.name}</td>
            <td>${u.email}</td>
            <td>${u.phone}</td>
            <td>${u.orders}</td>
            <td>
                <div class="table-actions">
                    <button class="btn-edit" title="ویرایش"><i class="fas fa-edit"></i></button>
                    <button class="btn-delete" title="حذف"><i class="fas fa-trash"></i></button>
                </div>
            </td>
        </tr>
    `).join('');
}

function renderCategories() {
    const tbody = document.getElementById('categories-table');
    if (!tbody) return;
    tbody.innerHTML = AdminAPI.categories.map(c => `
        <tr>
            <td>#${c.id}</td>
            <td><strong>${c.name}</strong></td>
            <td>/${c.slug}</td>
            <td>${c.parent ? AdminAPI.categories.find(x => x.id === c.parent)?.name || '-' : 'دسته اصلی'}</td>
            <td>
                <div class="table-actions">
                    <button class="btn-edit" title="ویرایش"><i class="fas fa-edit"></i></button>
                    <button class="btn-delete" onclick="AdminAPI.deleteCategory('${c.id}');renderCategories();" title="حذف"><i class="fas fa-trash"></i></button>
                </div>
            </td>
        </tr>
    `).join('');
}

function renderBrands() {
    const tbody = document.getElementById('brands-table');
    if (!tbody) return;
    tbody.innerHTML = AdminAPI.brands.map(b => `
        <tr>
            <td>#${b.id}</td>
            <td><strong>${b.name}</strong></td>
            <td>/${b.slug}</td>
            <td>
                <div class="table-actions">
                    <button class="btn-edit" title="ویرایش"><i class="fas fa-edit"></i></button>
                    <button class="btn-delete" onclick="AdminAPI.deleteBrand('${b.id}');renderBrands();" title="حذف"><i class="fas fa-trash"></i></button>
                </div>
            </td>
        </tr>
    `).join('');
}

function deleteProduct(id) {
    if (confirm('آیا از حذف این محصول اطمینان دارید؟')) {
        AdminAPI.deleteProduct(id);
        renderProducts();
    }
}

function editProduct(id) {
    alert('پنل ویرایش محصول - ID: ' + id);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.admin-layout')) {
        checkAuth();
        initAdminData();
        loadStats();
        renderProducts();
        renderOrders();
        renderUsers();
        renderCategories();
        renderBrands();
    }
});
