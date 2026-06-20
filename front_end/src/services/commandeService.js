const BASE = "/api/commandes"

export const commandeService = {

  getAll: async (statut = "tous") => {
    const url = statut === "tous"
      ? `${BASE}/`
      : `${BASE}/?statut=${statut}`

    const res = await fetch(url, {
      method: "GET",
      credentials: "include"
    })

    if (!res.ok) throw new Error("Erreur chargement commandes")
    return res.json()
  },

  confirmer: async () => {
    const res = await fetch("/api/paiement/checkout", {
      method: "POST",
      credentials: "include"
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.error || "Erreur paiement")
    }

    return res.json()
  },                          // ← virgule manquante ici

  telechargerRecu: (id) => {
    window.open(`/api/commandes/${id}/recu`, "_blank")
  }

}