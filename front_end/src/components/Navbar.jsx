import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

export default function Navbar({ panierCount = 0, backTo = null, backLabel = "← Retour" }) {
  const navigate   = useNavigate()
  const { logout } = useAuth()

  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-orange-500">🍔 Resto</h1>
      <div className="flex gap-3">

        {backTo && (
          <button
            onClick={() => navigate(backTo)}
            className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
          >
            {backLabel}
          </button>
        )}

        <button onClick={() => navigate('/panier')} className="relative px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition">
          🛒 Panier
          {panierCount > 0 && (
            <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
              {panierCount}
            </span>
          )}
        </button>

        <button onClick={() => navigate('/commandes')} className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition">
          📦 Commandes
        </button>

        <button onClick={async () => { await logout(); navigate('/') }} className="px-4 py-2 border border-red-800 rounded-lg text-red-400 hover:bg-red-950 transition">
          Déconnexion
        </button>

      </div>
    </nav>
  )
}