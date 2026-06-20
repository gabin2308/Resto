import { useNavigate } from "react-router-dom"

export default function PaiementCancel() {

  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">

      <div className="bg-gray-900 p-8 rounded-xl text-center">

        <h1 className="text-3xl text-red-500 font-bold mb-4">
          ❌ Paiement annulé
        </h1>

        <p className="text-gray-300 mb-6">
          Votre paiement a été annulé.
        </p>

        <button
          onClick={() => navigate("/panier")}
          className="bg-orange-500 hover:bg-orange-600 px-6 py-3 rounded-lg font-bold"
        >
          Retour au panier
        </button>

      </div>

    </div>
  )
}