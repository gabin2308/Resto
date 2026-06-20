import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { panierService } from "../services/panierService"
import { useAuth } from "../context/AuthContext"
import Navbar from "../components/Navbar"
import { commandeService } from "../services/commandeService"
import { paiementService } from "../services/paiementService"

export default function Panier() {
  const [panier,  setPanier]  = useState({ items: [], total: 0, count: 0 })
  const [loading, setLoading] = useState(true)
  const navigate              = useNavigate()
  const { user, loading: authLoading } = useAuth()
  const [confirming, setConfirming] = useState(false)

  useEffect(() => {
    if (!authLoading && !user) navigate('/')
  }, [user, authLoading])

  useEffect(() => {
    panierService.get()
      .then(data => {
        if (data.items) setPanier(data)
        else navigate('/')
      })
      .finally(() => setLoading(false))
  }, [])

    const refreshPanier = async () => {
    const data = await panierService.get()
    setPanier(data)
    }

  const handleSupprimer = async (id) => {
  try {
    await panierService.supprimer(id)
    await refreshPanier()

    } catch (error) {
        console.error("Erreur lors de la suppression :", error)
        }
    }
    const handleVider = async () => {
    try {
        await panierService.vider()
        await refreshPanier()

    } catch (error) {
        console.error("Erreur lors du vidage du panier :", error)
    }
    }
// 
//   const handleConfirmer = async () => {
//   try {
//     setConfirming(true)

//     const res = await commandeService.confirmer()

//     // Stripe URL
//     window.location.href = res.url

//   } catch (error) {
//     console.error(error)
//   } finally {
//     setConfirming(false)
//   }
// }
   const handleConfirmer = () => {
  localStorage.setItem("pending_order", JSON.stringify(panier))
  navigate("/paiement")
}

  if (loading) return <p className="text-white text-center mt-10">Chargement...</p>

  return (
    <div className="min-h-screen bg-gray-950 text-white">

      {/* Navbar */}
        <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center">
            <img src="/resto_logo.svg" alt="Resto" className="h-20" />
            <button
            onClick={() => navigate('/menu')}
            className="px-4 py-2 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition"
            >
            ← Menu
            </button>
        </nav>

      <div className="max-w-3xl mx-auto px-4 py-6">
        <h2 className="text-2xl font-bold mb-6">🛒 Mon Panier</h2>

        {panier.items.length === 0 ? (
          <div className="text-center text-gray-400 py-20">
            <p className="text-4xl mb-4">🍽️</p>
            <p>Ton panier est vide</p>
            <button
              onClick={() => navigate('/menu')}
              className="mt-6 bg-orange-500 hover:bg-orange-600 text-white font-bold px-6 py-3 rounded-lg transition"
            >
              Voir le menu
            </button>
          </div>
        ) : (
          <>
            {/* Liste items */}
            <div className="flex flex-col gap-3 mb-6">
              {panier.items.map(item => (
                <div key={item.id} className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">{item.nom}</h3>
                    <p className="text-gray-400 text-sm">x{item.quantite} — {item.prix} € / unité</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-orange-500 font-bold">
                      {(item.prix * item.quantite).toFixed(2)} €
                    </span>
                    <button
                      onClick={() => handleSupprimer(item.id)}
                      className="text-red-400 hover:text-red-300 text-sm transition"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Total */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex justify-between items-center mb-4">
              <span className="text-gray-400">Total</span>
              <span className="text-orange-500 font-bold text-xl">{panier.total} €</span>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={handleVider}
                className="flex-1 border border-red-800 text-red-400 hover:bg-red-950 py-3 rounded-lg transition"
              >
                Vider le panier
              </button>
             <button
            onClick={handleConfirmer}
            disabled={confirming}
            className="flex-1 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-lg transition"
            >
            {confirming ? "Commande en cours..." : "Commander →"}
            </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}