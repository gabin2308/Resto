import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { paiementService } from "../services/paiementService"
import { useAuth } from "../context/AuthContext"

export default function Historique() {
  const [paiements, setPaiements] = useState([])
  const [loading,   setLoading]   = useState(true)
  const [statut,    setStatut]    = useState("tous")
  const navigate = useNavigate()
  const { user, loading: authLoading } = useAuth()

  useEffect(() => {
    if (!authLoading && !user) navigate("/")
  }, [user, authLoading])

  useEffect(() => {
    paiementService.historique(statut)
      .then(data => {
        if (Array.isArray(data)) setPaiements(data)
        else setPaiements([])
      })
      .catch(() => setPaiements([]))
      .finally(() => setLoading(false))
  }, [statut])

  const getBadge = (s) => {
    switch (s) {
      case "payé":       return "bg-green-500/20 text-green-400"
      case "annulé":     return "bg-red-500/20 text-red-400"
      case "en attente": return "bg-yellow-500/20 text-yellow-400"
      default:           return "bg-gray-500/20 text-gray-400"
    }
  }

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      Chargement...
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-white">

      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-orange-500">💳 Historique des paiements</h1>
        <button
          onClick={() => navigate("/commandes")}
          className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
        >
          ← Commandes
        </button>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-6">

        {/* Filtres */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {["tous", "payé", "en attente", "annulé"].map(s => (
            <button
              key={s}
              onClick={() => setStatut(s)}
              className={`px-4 py-2 rounded-full text-sm border transition ${
                statut === s
                  ? "bg-orange-500 border-orange-500 text-white"
                  : "border-gray-700 text-gray-300 hover:border-orange-500"
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        {/* Liste */}
        {paiements.length === 0 ? (
          <div className="text-center text-gray-400 py-20">
            <p className="text-4xl mb-4">💳</p>
            <p>Aucun paiement trouvé</p>
          </div>
        ) : (
          <div className="space-y-4">
            {paiements.map(p => (
              <div key={p.id} className="bg-gray-900 border border-gray-800 rounded-xl p-4">

                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-bold text-orange-500">
                    Paiement #{p.id}
                  </h3>
                  <span className={`text-sm px-3 py-1 rounded-full ${getBadge(p.statut)}`}>
                    {p.statut}
                  </span>
                </div>

                <p className="text-gray-400 text-sm">Date : {p.date}</p>
                <p className="text-gray-400 text-sm">
                  Commande : <span className="text-white">#{p.id_commande}</span>
                </p>
                <p className="text-gray-400 text-sm">
                  Stripe ID : <span className="text-gray-500 text-xs">{p.stripe_id || "—"}</span>
                </p>
                <p className="text-gray-400 text-sm mt-1">
                  Montant : <span className="text-orange-500 font-bold">{p.montant} €</span>
                </p>

              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  )
}