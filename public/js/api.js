// DotWatch API Client
const API_BASE = '';

function getToken() {
  return localStorage.getItem('token') || '';
}

async function apiFetch(url, options = {}) {
  const opts = {
    headers: {
      'Content-Type': 'application/json',
      ...(getToken() ? { 'Authorization': 'Bearer ' + getToken() } : {})
    },
    ...options
  };
  if (opts.body && typeof opts.body === 'object') {
    opts.body = JSON.stringify(opts.body);
  }
  try {
    const res = await fetch(API_BASE + url, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Request failed' }));
      console.error('API Error:', url, err);
      throw new Error(err.error || 'Request failed');
    }
    return res.json();
  } catch (e) {
    console.error('Network Error:', url, e.message);
    throw e;
  }
}

function transformProduct(p) {
  if (!p) return p;
  return {
    ...p,
    isNew: p.is_new,
    oldPrice: p.old_price,
    brand: p.brand_id,
    brandFa: p.brandFa || p.brand_fa,
    specs: {
      movement: p.movement,
      diameter: p.diameter,
      thickness: p.thickness,
      case: p.case_material,
      band: p.band_material,
      glass: p.glass,
      water: p.water_resistant,
      weight: p.weight,
      functions: p.functions
    }
  };
}

const API = {
  Products: {
    list: async (params = {}) => {
      const qs = new URLSearchParams(params).toString();
      const data = await apiFetch('/api/products?' + qs);
      return Array.isArray(data) ? data.map(transformProduct) : [];
    },
    get: async (id) => {
      const data = await apiFetch('/api/products/' + id);
      return transformProduct(data);
    },
    reviews: (id) => apiFetch('/api/products/' + id + '/reviews'),
    addReview: (id, data) => apiFetch('/api/products/' + id + '/reviews', { method: 'POST', body: data })
  },
  Auth: {
    register: (data) => apiFetch('/api/auth/register', { method: 'POST', body: data }),
    login: (data) => apiFetch('/api/auth/login', { method: 'POST', body: data }),
    me: () => apiFetch('/api/auth/me')
  },
  Cart: {
    get: () => apiFetch('/api/cart'),
    add: (data) => apiFetch('/api/cart', { method: 'POST', body: data }),
    update: (product_id, data) => apiFetch('/api/cart/' + product_id, { method: 'PUT', body: data }),
    remove: (product_id) => apiFetch('/api/cart/' + product_id, { method: 'DELETE' })
  },
  Wishlist: {
    get: () => apiFetch('/api/wishlist'),
    toggle: (data) => apiFetch('/api/wishlist', { method: 'POST', body: data }),
    remove: (product_id) => apiFetch('/api/wishlist/' + product_id, { method: 'DELETE' })
  },
  Orders: {
    list: () => apiFetch('/api/orders'),
    get: (id) => apiFetch('/api/orders/' + id),
    create: (data) => apiFetch('/api/orders', { method: 'POST', body: data })
  },
  Articles: {
    list: () => apiFetch('/api/articles'),
    get: (id) => apiFetch('/api/articles/' + id)
  },
  Brands: {
    list: () => apiFetch('/api/brands')
  },
  Accessories: {
    list: () => apiFetch('/api/accessories')
  },
  FAQs: {
    list: () => apiFetch('/api/faqs')
  },
  Banners: {
    list: (position) => apiFetch('/api/banners' + (position ? '?position=' + position : ''))
  },
  Menus: {
    list: () => apiFetch('/api/menus')
  },
  FooterLinks: {
    list: () => apiFetch('/api/footer-links')
  },
  PageTexts: {
    list: () => apiFetch('/api/page-texts'),
    get: (section) => apiFetch('/api/page-texts/' + section)
  },
  Settings: {
    get: () => apiFetch('/api/settings')
  },
  Addresses: {
    list: () => apiFetch('/api/addresses'),
    create: (data) => apiFetch('/api/addresses', { method: 'POST', body: data }),
    update: (id, data) => apiFetch('/api/addresses/' + id, { method: 'PUT', body: data }),
    remove: (id) => apiFetch('/api/addresses/' + id, { method: 'DELETE' })
  },
  Admin: {
    getData: () => apiFetch('/api/admin/data'),
    getStats: () => apiFetch('/api/admin/stats'),
    getBackup: () => apiFetch('/api/admin/backup')
  }
};

window.API = API;

// DB object for frontend compatibility
window.DB = {
  products: [],
  brands: [],
  articles: [],
  accessories: [],
  faqs: [],
  banners: [],
  menus: [],
  footerLinks: [],
  pageTexts: {},
  settings: {}
};

// Load data only when called, not automatically
window.loadAPIData = async function() {
  try {
    const [products, brands, articles, accessories, faqs, banners, menus, footerLinks, pageTexts, settings] = await Promise.all([
      API.Products.list({ limit: 100 }).catch(() => []),
      API.Brands.list().catch(() => []),
      API.Articles.list().catch(() => []),
      API.Accessories.list().catch(() => []),
      API.FAQs.list().catch(() => []),
      API.Banners.list().catch(() => []),
      API.Menus.list().catch(() => []),
      API.FooterLinks.list().catch(() => []),
      API.PageTexts.list().catch(() => ({})),
      API.Settings.get().catch(() => ({}))
    ]);
    window.DB.products = products;
    window.DB.brands = brands;
    window.DB.articles = articles;
    window.DB.accessories = accessories;
    window.DB.faqs = faqs;
    window.DB.banners = banners;
    window.DB.menus = menus;
    window.DB.footerLinks = footerLinks;
    window.DB.pageTexts = pageTexts;
    window.DB.settings = settings;
    console.log('✅ DB loaded from API');
  } catch (e) {
    console.error('❌ Failed to load API data:', e);
  }
};
