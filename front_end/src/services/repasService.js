const BASE = "/api/repas";

export const repasService = {
  getAll: async (cat = '') => {
    const url = cat ? `${BASE}/?cat=${cat}` : `${BASE}/`;
    const res = await fetch(url, { credentials: "include" });
    return res.json();
  },

  getCategories: async () => {
    const res = await fetch(`${BASE}/categories`, { credentials: "include" });
    return res.json();
  },

  recherche: async (search) => {
    const res = await fetch(`${BASE}/recherche?search=${search}`, { credentials: "include" });
    return res.json();
  }
};