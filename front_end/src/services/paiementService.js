const BASE = "/api/paiement";

export const paiementService = {
  getPanier: async () => {
    const res = await fetch(`${BASE}/`, {
      credentials: "include"
    });

    return res.json();
  },

  checkout: async () => {
    const res = await fetch(`${BASE}/checkout`, {
      method: "POST",
      credentials: "include"
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Erreur checkout");
    }

    return res.json();
  },

  success: async (session_id) => {
    const res = await fetch(`${BASE}/success?session_id=${session_id}`, {
      credentials: "include"
    });

    return res.json();
  },
  historique: async (statut = "tous") => {
  const url = statut === "tous"
    ? `${BASE}/historique`
    : `${BASE}/historique?statut=${statut}`

  const res = await fetch(url, { credentials: "include" })
  if (!res.ok) throw new Error("Erreur historique")
  return res.json()
}
};