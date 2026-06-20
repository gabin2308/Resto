import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { commandeService } from "../services/commandeService"

export default function Commandes() {

  // commandes affichées
  const [commandes, setCommandes] = useState([])

  // toutes les commandes
  const [commandesFull, setCommandesFull] = useState([])

  const [loading, setLoading] = useState(true)

  // filtre statut
  const [statut, setStatut] = useState("tous")

  // recherche
  const [search, setSearch] = useState("")

  const navigate = useNavigate()

  const { user, loading: authLoading } = useAuth()

  // vérification connexion utilisateur
  useEffect(() => {

    if (!authLoading && !user) {
      navigate("/")
    }

  }, [user, authLoading, navigate])

  // chargement initial UNE seule fois
  useEffect(() => {
    loadCommandes()
  }, [])

  // récupération commandes
  const loadCommandes = async () => {

    try {

      setLoading(true)

      const data = await commandeService.getAll()

      if (Array.isArray(data)) {

        // sauvegarde complète
        setCommandesFull(data)

        // affichage initial
        setCommandes(data)

      } else {

        setCommandes([])
        setCommandesFull([])

      }

    } catch (error) {

      console.error(error)

      setCommandes([])
      setCommandesFull([])

    } finally {

      setLoading(false)

    }
  }

  // filtrage LOCAL
  // se déclenche quand :
  // - statut change
  // - recherche change
  // - données changent
  useEffect(() => {

    let filtered = [...commandesFull]

    // =========================
    // filtre par statut
    // =========================
    if (statut !== "tous") {

      filtered = filtered.filter(cmd =>
        cmd.statut === statut
      )
    }

    // =========================
    // filtre recherche
    // =========================
    if (search.trim()) {

      filtered = filtered.filter(cmd =>

        // recherche sur id commande
        String(cmd.id).includes(search)

        ||

        // recherche sur statut
        cmd.statut
          ?.toLowerCase()
          .includes(search.toLowerCase())
      )
    }

    // mise à jour affichage
    setCommandes(filtered)

  }, [statut, search, commandesFull])

  // gestion recherche
  const handleSearch = (e) => {
    setSearch(e.target.value)
  }

  // couleurs badge statut
  const getBadgeClass = (s) => {

    switch (s) {

      case "en attente":
        return "bg-yellow-500/20 text-yellow-400"

      case "en cours":
        return "bg-blue-500/20 text-blue-400"

      case "livrée":
        return "bg-green-500/20 text-green-400"

      case "annulée":
        return "bg-red-500/20 text-red-400"

      default:
        return "bg-gray-500/20 text-gray-400"
    }
  }

  // écran chargement
  if (loading) {

    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
        Chargement des commandes...
      </div>
    )
  }

  return (

    <div className="min-h-screen bg-gray-950 text-white">

      {/* NAVBAR */}
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center">

        <h1 className="text-2xl font-bold text-orange-500">
          📦 Mes Commandes
        </h1>

        <div className="flex gap-3">

          <button
            onClick={() => navigate("/menu")}
            className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
          >
            ← Menu
          </button>

          <button
            onClick={() => navigate("/historique")}
            className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
          >
            💳 Historique paiements
          </button>

        </div>

      </nav>

      <div className="max-w-4xl mx-auto px-4 py-6">

        {/* ========================= */}
        {/* RECHERCHE */}
        {/* ========================= */}
        <input
          type="text"
          placeholder="Rechercher une commande..."
          value={search}
          onChange={handleSearch}
          className="w-full mb-6 bg-gray-900 border border-gray-700 text-white px-4 py-3 rounded-lg outline-none focus:border-orange-500 transition"
        />

        {/* ========================= */}
        {/* FILTRES */}
        {/* ========================= */}
        <div className="flex gap-2 mb-6 flex-wrap">

          {["tous", "en attente", "en cours", "livrée", "annulée"].map(s => (

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

        {/* compteur */}
        <p className="text-gray-400 text-sm mb-4">
          {commandes.length} commande(s) trouvée(s)
        </p>

        {/* ========================= */}
        {/* LISTE COMMANDES */}
        {/* ========================= */}
        {commandes.length === 0 ? (

          <div className="text-center text-gray-400 py-20">

            <p className="text-4xl mb-4">📦</p>

            <p>Aucune commande trouvée</p>

            <button
              onClick={() => navigate("/menu")}
              className="mt-6 bg-orange-500 hover:bg-orange-600 text-white font-bold px-6 py-3 rounded-lg transition"
            >
              Commander maintenant
            </button>

          </div>

        ) : (

          <div className="space-y-4">

            {commandes.map(cmd => (

              <div
                key={cmd.id}
                className="bg-gray-900 border border-gray-800 rounded-xl p-4"
              >

                {/* HEADER */}
                <div className="flex justify-between items-center mb-2">

                  <h3 className="font-bold text-orange-500">
                    Commande #{cmd.id}
                  </h3>

                  <span className={`text-sm px-3 py-1 rounded-full ${getBadgeClass(cmd.statut)}`}>
                    {cmd.statut}
                  </span>

                </div>

                {/* infos */}
                <p className="text-gray-400 text-sm">
                  Date : {cmd.date}
                </p>

                <p className="text-gray-400 text-sm">
                  Total :
                  <span className="text-orange-500 font-bold ml-1">
                    {cmd.total} €
                  </span>
                </p>

                {/* ========================= */}
                {/* ITEMS */}
                {/* ========================= */}
                {cmd.items?.length > 0 && (

                  <div className="mt-3 border-t border-gray-800 pt-3 space-y-1">

                    {cmd.items.map((item, index) => (

                      <div
                        key={index}
                        className="flex justify-between text-sm text-gray-300"
                      >

                        <span>
                          {item.nom} x{item.quantite}
                        </span>

                        <span className="text-orange-400">
                          {(item.prix * item.quantite).toFixed(2)} €
                        </span>

                      </div>

                    ))}

                  </div>

                )}

                {/* ========================= */}
                {/* REÇU PDF */}
                {/* ========================= */}
                <div className="mt-3 pt-3 border-t border-gray-800">

                  <a
                    href={`/api/commandes/${cmd.id}/recu`}
                    download={`recu_commande_${cmd.id}.pdf`}
                    className="inline-block text-sm text-orange-500 hover:text-orange-400 border border-orange-800 hover:border-orange-500 px-4 py-2 rounded-lg transition"
                  >
                    📄 Télécharger le reçu
                  </a>

                </div>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>
  )
}