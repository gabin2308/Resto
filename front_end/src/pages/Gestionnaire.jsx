import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

const BASE = "/api/gestionnaire"

export default function Gestionnaire() {

  const [commandes, setCommandes] = useState([])
  const [commandesFull, setCommandesFull] = useState([])
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [statut, setStatut] = useState("tous")
  const [search, setSearch] = useState("")

  const navigate = useNavigate()
  const { user, loading: authLoading } = useAuth()

  // Vérification auth
  useEffect(() => {

    if (!authLoading && !user) {
      navigate("/")
    }

    if (
      !authLoading &&
      user &&
      user.role !== "gestionnaire" &&
      user.role !== "admin"
    ) {
      navigate("/menu")
    }

  }, [user, authLoading, navigate])

  // Chargement initial
  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {

    try {

      setLoading(true)

      const res = await fetch(`${BASE}/`, {
        credentials: "include"
      })

      const data = await res.json()

      if (data.commandes) {
        setCommandes(data.commandes)
        setCommandesFull(data.commandes)
      }

      if (data.users) {
        setUsers(data.users)
      }

    } catch (error) {

      console.error(error)

    } finally {

      setLoading(false)

    }
  }

  // Filtrage local
  useEffect(() => {

    let filtered = [...commandesFull]

    // filtre statut
    if (statut !== "tous") {
      filtered = filtered.filter(c => c.statut === statut)
    }

    // filtre recherche
    if (search.trim()) {

      filtered = filtered.filter(c => {

        const u = users.find(u => u.id === c.user_id)

        return (
          String(c.user_id).includes(search) ||
          u?.username?.toLowerCase().includes(search.toLowerCase())
        )
      })
    }

    setCommandes(filtered)

  }, [statut, search, commandesFull, users])

  // Recherche
  const handleSearch = (e) => {
    setSearch(e.target.value)
  }

  // Changement statut
  const handleStatut = async (id, user_id, nouveau_statut) => {

    try {

      await fetch(`${BASE}/commandes/${id}/statut`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
          statut: nouveau_statut,
          user_id
        })
      })

      // mise à jour locale
      const updated = commandesFull.map(c =>
        c.id === id
          ? { ...c, statut: nouveau_statut }
          : c
      )

      setCommandesFull(updated)

    } catch (error) {

      console.error(error)

    }
  }

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
        Chargement...
      </div>
    )
  }

  return (

    <div className="min-h-screen bg-gray-950 text-white">

      {/* NAVBAR */}
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center">

        <img
          src="/resto_logo.svg"
          alt="Resto"
          className="h-20"
        />

        <h2 className="text-lg font-semibold text-white">
          Espace Gestionnaire
        </h2>

        <button
          onClick={() => navigate("/menu")}
          className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
        >
          ← Menu
        </button>

      </nav>

      <div className="max-w-5xl mx-auto px-4 py-6 space-y-6">

        {/* RECHERCHE */}
        <input
          type="text"
          placeholder="Rechercher par nom d'utilisateur..."
          value={search}
          onChange={handleSearch}
          className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-3 rounded-lg outline-none focus:border-orange-500 transition"
        />

        {/* FILTRES */}
        <div className="flex gap-2 flex-wrap">

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

        {/* COMPTEUR */}
        <p className="text-gray-400 text-sm">
          {commandes.length} commande(s) trouvée(s)
        </p>

        {/* LISTE */}
        {commandes.length === 0 ? (

          <div className="text-center text-gray-400 py-20">

            <p className="text-4xl mb-4">📦</p>

            <p>Aucune commande trouvée</p>

          </div>

        ) : (

          <div className="space-y-4">

            {commandes.map(cmd => (

              <div
                key={cmd.id}
                className="bg-gray-900 border border-gray-800 rounded-xl p-4"
              >

                {/* HEADER */}
                <div className="flex justify-between items-center mb-3">

                  <div>

                    <h3 className="font-bold text-orange-500">
                      Commande #{cmd.id}
                    </h3>

                    <p className="text-gray-400 text-sm">
                      Client :
                      <span className="text-white ml-1">
                        {
                          users.find(u => u.id === cmd.user_id)?.username
                          || `User #${cmd.user_id}`
                        }
                      </span>
                    </p>

                    <p className="text-gray-400 text-sm">
                      Date : {cmd.date}
                    </p>

                    <p className="text-gray-400 text-sm">
                      Total :
                      <span className="text-orange-500 font-bold ml-1">
                        {cmd.total} €
                      </span>
                    </p>

                  </div>

                  <span className={`text-sm px-3 py-1 rounded-full ${getBadgeClass(cmd.statut)}`}>
                    {cmd.statut}
                  </span>

                </div>

                {/* ITEMS */}
                {cmd.items?.length > 0 && (

                  <div className="border-t border-gray-800 pt-3 mb-3 space-y-1">

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

                {/* ACTIONS */}
                <div className="flex gap-2 flex-wrap border-t border-gray-800 pt-3">

                  {["en attente", "en cours", "livrée", "annulée"].map(s => (

                    <button
                      key={s}
                      onClick={() => handleStatut(cmd.id, cmd.user_id, s)}
                      disabled={cmd.statut === s}
                      className={`px-3 py-1 rounded-lg text-xs border transition ${
                        cmd.statut === s
                          ? "border-orange-500 text-orange-500 cursor-not-allowed"
                          : "border-gray-700 text-gray-300 hover:border-orange-500 hover:text-orange-500"
                      }`}
                    >
                      {s}
                    </button>

                  ))}

                </div>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>
  )
}