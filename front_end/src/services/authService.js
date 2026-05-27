const BASE = "/api/auth";

export const authService = {
  login: async (username, password) => {
    const res = await fetch(`${BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, password })
    });

    if(res.status === 429) {
      return {error: "Trop de tentatives, réessaye plus tard.", status: 429}
    }
    return res.json();
  },

  register: async (username, password) => {
    const res = await fetch(`${BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, password })
    });
    if(res.status === 429) {
      return {error: "Trop de tentatives, réessaye plus tard.", status: 429}
    }
    return res.json();
  },

  logout: async () => {
    const res = await fetch(`${BASE}/logout`, { method: "POST", credentials: "include" });
    return res.json();
  },

  me: async () => {
    const res = await fetch(`${BASE}/me`, { credentials: "include" });
    return res.json();
  }
};