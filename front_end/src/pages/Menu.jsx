import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { repasService } from "../services/repasService"
import { panierService } from "../services/panierService"
import { useAuth } from "../context/AuthContext"

export default function Menu() {
  const [repas,      setRepas]      = useState([])
  const [categories, setCategories] = useState([])
  const [catActive,  setCatActive]  = useState("tous")
  const [search,     setSearch]     = useState("")
  const [loading,    setLoading]    = useState(true)
  const navigate                    = useNavigate()
  const {user}                       = useAuth()

    // Redirige vers login si pas connecté
    useEffect(() => {
        if (!user) navigate('/')
        }, [user])

//   // Chargement initial
//   useEffect(() => {
//     repasService.getCategories().then(setCategories)
//     repasService.getAll().then(setRepas).finally(() => setLoading(false))
//   }, [])

//   // Filtre par catégorie
//   useEffect(() => {
//     repasService.getAll(catActive).then(setRepas)
//   }, [catActive])

    // Chargement initial
    useEffect(() => {
    repasService.getCategories().then(data => {
        if (Array.isArray(data)) setCategories(data)
    })
    repasService.getAll().then(data => {
        if (Array.isArray(data)) setRepas(data)
        else navigate('/')
    }).finally(() => setLoading(false))
    }, [])

    useEffect(() => {
        repasService.getAll(catActive).then(data => {
            if (Array.isArray(data)) setRepas(data)
        })
        }, [catActive])

  // Recherche
  const handleSearch = async (e) => {
    const val = e.target.value
    setSearch(val)
    if (val) {
      repasService.recherche(val).then(setRepas)
    } else {
      repasService.getAll(catActive).then(setRepas)
    }
  }

  const handleAjouter = async (repas) => {
    await panierService.ajouter(repas.id, repas.nom, repas.prix, 1)
    navigate('/panier')
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div className="menu-page">

      {/* Navbar */}
      <nav className="navbar">
        <h1>🍔 Resto</h1>
        <div className="nav-links">
          <button onClick={() => navigate('/panier')}>🛒 Panier</button>
          <button onClick={() => navigate('/commandes')}>📦 Commandes</button>
        </div>
      </nav>

      {/* Recherche */}
      <input
        type="text"
        placeholder="Rechercher un repas..."
        value={search}
        onChange={handleSearch}
        className="search-input"
      />

      {/* Filtres catégories */}
      <div className="categories">
        {["tous", ...categories].map(cat => (
          <button
            key={cat}
            className={`cat-btn ${catActive === cat ? 'active' : ''}`}
            onClick={() => setCatActive(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Liste repas */}
      <div className="repas-grid">
        {repas.map(r => (
          <div key={r.id} className="repas-card">
            {r.photo && (
              <img src={`/static/img/${r.photo}`} alt={r.nom} />
            )}
            <div className="repas-info">
              <h3>{r.nom}</h3>
              <p>{r.description}</p>
              <span className="prix">{r.prix} €</span>
              <span className={`statut ${r.statut}`}>{r.statut}</span>
            </div>
            <button
              onClick={() => handleAjouter(r)}
              disabled={r.statut === 'indisponible'}
            >
              Ajouter au panier
            </button>
          </div>
        ))}
      </div>

    </div>
  )
}