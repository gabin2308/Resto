const BASE = "/api/panier";

export const panierService = {
  get: async () => {
    const res = await fetch(`${BASE}/`, { credentials: "include" });
    return res.json();
  },

  ajouter: async (id, nom, prix, quantite = 1) => {
    const res = await fetch(`${BASE}/ajouter`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ id, nom, prix, quantite })
    });
    return res.json();
  },

  supprimer: async (id) => {
    const res = await fetch(`${BASE}/supprimer/${id}`, { method: "DELETE", credentials: "include" });
    return res.json();
  },

  vider: async () => {
    const res = await fetch(`${BASE}/vider`, { method: "DELETE", credentials: "include" });
    return res.json();
  }
};