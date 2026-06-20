import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { repasService } from "../services/repasService"
import { panierService } from "../services/panierService"
import { commandeService } from "../services/commandeService"
import { useAuth } from "../context/AuthContext"

export default function Menu() {

  // ==============================
  // STATES
  // ==============================

  const [repas, setRepas] = useState([])

  const [categories, setCategories] = useState([])

  // catégorie active
  const [catActive, setCatActive] = useState("tous")

  // recherche
  const [search, setSearch] = useState("")

  // loading page
  const [loading, setLoading] = useState(true)

  // compteur panier
  const [panierCount, setPanierCount] = useState(0)

  // compteur commandes
  const [commandesCount, setCommandesCount] = useState(0)

  const navigate = useNavigate()

  const {
    user,
    loading: authLoading,
    logout
  } = useAuth()

  // ==============================
  // REDIRECTION SI PAS CONNECTÉ
  // ==============================
  useEffect(() => {

    if (!authLoading && !user) {
      navigate("/")
    }

  }, [user, authLoading, navigate])

  // ==============================
  // CHARGEMENT INITIAL
  // ==============================
  useEffect(() => {

    // récupération catégories
    repasService.getCategories().then(data => {

      if (Array.isArray(data)) {
        setCategories(data)
      }

    })

    // récupération repas
    repasService.getAll()
      .then(data => {

        if (Array.isArray(data)) {

          setRepas(data)

        } else {

          navigate("/")

        }

      })
      .finally(() => setLoading(false))

    // récupération panier
    panierService.get().then(data => {

      if (data.count) {
        setPanierCount(data.count)
      }

    })

    // récupération commandes utilisateur
    commandeService.getAll().then(data => {

      if (Array.isArray(data)) {

        // commandes actives uniquement
        const active = data.filter(cmd =>
          cmd.statut !== "livrée" &&
          cmd.statut !== "annulée"
        )

        setCommandesCount(active.length)
      }

    })

  }, [])

  // ==============================
  // FILTRE PAR CATÉGORIE
  // ==============================
  useEffect(() => {

    repasService.getAll(catActive).then(data => {

      if (Array.isArray(data)) {
        setRepas(data)
      }

    })

  }, [catActive])

  // ==============================
  // RECHERCHE
  // ==============================
  const handleSearch = async (e) => {

    const val = e.target.value

    setSearch(val)

    // si recherche vide
    if (!val) {

      repasService.getAll(catActive).then(setRepas)

      return
    }

    // recherche repas
    repasService.recherche(val).then(setRepas)
  }

  // ==============================
  // AJOUT PANIER
  // ==============================
  const handleAjouter = async (repas) => {

    try {

      await panierService.ajouter(
        repas.id,
        repas.nom,
        repas.prix,
        1
      )

      // update panier badge
      setPanierCount(prev => prev + 1)

      // refresh commandes
      commandeService.getAll().then(data => {

        if (Array.isArray(data)) {

          const active = data.filter(cmd =>
            cmd.statut !== "livrée"
            //  &&
            // cmd.statut !== "annulée"
          )

          setCommandesCount(active.length)
        }

      })

    } catch (error) {

      console.error(error)

    }
  }

  // ==============================
  // LOADING
  // ==============================
  if (loading) {

    return (
      <p className="text-white text-center mt-10">
        Chargement...
      </p>
    )
  }

  return (

    <div className="min-h-screen bg-gray-950 text-white">

      {/* ============================== */}
      {/* NAVBAR */}
      {/* ============================== */}
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center">

        {/* logo */}
        <img
          src="/resto_logo.svg"
          alt="Resto"
          className="h-20"
        />

        <div className="flex gap-3">

          {/* ============================== */}
          {/* PANIER */}
          {/* ============================== */}
          <button
            onClick={() => navigate("/panier")}
            className="relative px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
          >

            🛒 Panier

            {/* badge panier */}
            {panierCount > 0 && (

              <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
                {panierCount}
              </span>

            )}

          </button>

          {/* ============================== */}
          {/* COMMANDES */}
          {/* ============================== */}
          <button
            onClick={() => navigate("/commandes")}
            className="relative px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
          >

            📦 Commandes

            {/* badge commandes */}
            {commandesCount > 0 && (

              <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
                {commandesCount}
              </span>

            )}

          </button>

          {/* ============================== */}
          {/* GESTION */}
          {/* ============================== */}
          {(user?.role === "gestionnaire" || user?.role === "admin") && (

            <button
              onClick={() => navigate("/gestionnaire")}
              className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
            >
              🛠 Gestion
            </button>

          )}

          {/* ============================== */}
          {/* LOGOUT */}
          {/* ============================== */}
          <button
            onClick={async () => {

              await logout()

              navigate("/")

            }}
            className="px-4 py-2 border border-red-800 rounded-lg text-red-400 hover:bg-red-950 transition"
          >
            Déconnexion
          </button>

        </div>

      </nav>

      {/* ============================== */}
      {/* CONTENU */}
      {/* ============================== */}
      <div className="max-w-6xl mx-auto px-4 py-6">

        {/* ============================== */}
        {/* RECHERCHE */}
        {/* ============================== */}
        <input
          type="text"
          placeholder="Rechercher un repas..."
          value={search}
          onChange={handleSearch}
          className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-3 rounded-lg outline-none focus:border-orange-500 transition mb-6"
        />

        {/* ============================== */}
        {/* FILTRES CATÉGORIES */}
        {/* ============================== */}
        <div className="flex gap-2 flex-wrap mb-6">

          {["tous", ...categories].map(cat => (

            <button
              key={cat}
              onClick={() => setCatActive(cat)}
              className={`px-4 py-2 rounded-full text-sm border transition ${
                catActive === cat
                  ? "bg-orange-500 border-orange-500 text-white"
                  : "bg-gray-900 border-gray-700 text-gray-300 hover:border-orange-500"
              }`}
            >
              {cat}
            </button>

          ))}

        </div>

        {/* ============================== */}
        {/* GRILLE REPAS */}
        {/* ============================== */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">

          {repas.map(r => (

            <div
              key={r.id}
              className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden flex flex-col"
            >

              {/* image */}
              {r.photo ? (

                <img
                  src={`/static/img/${r.photo}`}
                  alt={r.nom}
                  className="w-full h-44 object-cover"
                />

              ) : (

                <div className="w-full h-44 bg-gray-800 flex items-center justify-center text-4xl">
                  🍽️
                </div>

              )}

              {/* contenu */}
              <div className="p-4 flex flex-col gap-2 flex-1">

                <h3 className="font-semibold text-white">
                  {r.nom}
                </h3>

                <p className="text-gray-400 text-sm flex-1">
                  {r.description}
                </p>

                <span className="text-orange-500 font-bold text-lg">
                  {r.prix} €
                </span>

                <span className={`text-xs font-medium ${
                  r.statut === "disponible"
                    ? "text-green-400"
                    : "text-red-400"
                }`}>
                  {r.statut}
                </span>

              </div>

              {/* bouton ajout */}
              <button
                onClick={() => handleAjouter(r)}
                disabled={r.statut === "indisponible"}
                className="mx-4 mb-4 bg-orange-500 hover:bg-orange-600 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold py-2 rounded-lg transition"
              >
                Ajouter au panier
              </button>

            </div>

          ))}

        </div>

      </div>

    </div>
  )
}