import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { paiementService } from "../services/paiementService"

export default function PaiementSuccess() {
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const sessionId = new URLSearchParams(window.location.search).get("session_id")

    paiementService.success(sessionId)
      .then(data => {
        if (!data.success) setError(data.error)
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      Confirmation en cours...
    </div>
  )

  if (error) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      <div className="bg-gray-900 p-8 rounded-xl text-center">
        <h1 className="text-2xl text-red-500 font-bold mb-4">❌ Erreur</h1>
        <p className="text-gray-300">{error}</p>
        <button
          onClick={() => navigate('/panier')}
          className="mt-6 bg-orange-500 px-6 py-3 rounded-lg font-bold"
        >
          Retour au panier
        </button>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      <div className="bg-gray-900 p-8 rounded-xl text-center space-y-4">
        <h1 className="text-3xl text-green-500 font-bold">✅ Paiement réussi</h1>
        <p className="text-gray-300">Merci pour votre commande.</p>
        <div className="flex gap-3 justify-center mt-4">
          <button
            onClick={() => navigate('/commandes')}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-lg transition"
          >
            Voir mes commandes
          </button>
          <button
            onClick={() => navigate('/menu')}
            className="px-6 py-3 border border-gray-700 hover:border-orange-500 text-gray-300 hover:text-orange-500 rounded-lg transition"
          >
            Retour au menu
          </button>
        </div>
      </div>
    </div>
  )
}