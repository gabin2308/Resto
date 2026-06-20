// import { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { paiementService } from "../services/paiementService";
// import { useAuth } from "../context/AuthContext";

// export default function Paiement() {
//   const [panier, setPanier] = useState({ items: [], total: 0 });
//   const [loading, setLoading] = useState(true);
//   const [paying, setPaying] = useState(false);

//   const navigate = useNavigate();
//   const { user, loading: authLoading } = useAuth();

//   // 🔐 protection route
//   useEffect(() => {
//     if (!authLoading && !user) {
//       navigate("/");
//     }
//   }, [user, authLoading]);

//   // 📦 charger panier
//   useEffect(() => {
//     paiementService.getPanier()
//       .then(data => setPanier(data))
//       .catch(err => console.error(err))
//       .finally(() => setLoading(false));
//   }, []);

//   // 💳 checkout stripe
//   const handlePaiement = async () => {
//     try {
//       setPaying(true);

//       const { url } = await paiementService.checkout();

//       // redirection vers Stripe
//       window.location.href = url;

//     } catch (error) {
//       console.error("Erreur paiement :", error);
//       alert(error.message);
//     } finally {
//       setPaying(false);
//     }
//   };

//   if (loading) {
//     return (
//       <p className="text-center text-white mt-10">
//         Chargement du paiement...
//       </p>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gray-950 text-white p-6">

//       <h1 className="text-2xl font-bold text-orange-500 mb-6">
//         💳 Paiement
//       </h1>

//       {/* panier vide */}
//       {panier.items.length === 0 ? (
//         <div className="text-center text-gray-400 mt-20">
//           <p>Ton panier est vide</p>

//           <button
//             onClick={() => navigate("/menu")}
//             className="mt-4 bg-orange-500 px-4 py-2 rounded-lg"
//           >
//             Voir le menu
//           </button>
//         </div>
//       ) : (
//         <>
//           {/* LISTE PRODUITS */}
//           <div className="space-y-3 mb-6">
//             {panier.items.map((item) => (
//               <div
//                 key={item.id}
//                 className="flex justify-between bg-gray-900 p-3 rounded-lg"
//               >
//                 <div>
//                   <p className="font-semibold">{item.nom}</p>
//                   <p className="text-sm text-gray-400">
//                     {item.quantite} x {item.prix} €
//                   </p>
//                 </div>

//                 <p className="text-orange-400 font-bold">
//                   {(item.quantite * item.prix).toFixed(2)} €
//                 </p>
//               </div>
//             ))}
//           </div>

//           {/* TOTAL */}
//           <div className="flex justify-between border-t border-gray-700 pt-4 mb-6">
//             <p className="text-gray-400">Total</p>
//             <p className="text-xl text-orange-500 font-bold">
//               {panier.total} €
//             </p>
//           </div>

//           {/* BTN PAYER */}
//           <button
//             onClick={handlePaiement}
//             disabled={paying}
//             className="w-full bg-orange-500 hover:bg-orange-600 py-3 rounded-lg font-bold disabled:opacity-50"
//           >
//             {paying ? "Redirection..." : "Payer avec Stripe 💳"}
//           </button>
//         </>
//       )}
//     </div>
//   );
// }

import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { paiementService } from "../services/paiementService"

export default function Paiement() {

  const [panier, setPanier] = useState({
    items: [],
    total: 0
  })

  const [loading, setLoading] = useState(true)
  const [paying, setPaying] = useState(false)

  const navigate = useNavigate()

  useEffect(() => {

    paiementService.getPanier()
      .then(data => {
        setPanier(data)
      })
      .catch(err => {
        console.error(err)
        navigate("/panier")
      })
      .finally(() => {
        setLoading(false)
      })

  }, [])

  const handlePaiement = async () => {

    try {

      setPaying(true)

      const res = await paiementService.checkout()

      // 🔥 redirection Stripe
      window.location.href = res.url

    } catch (error) {

      console.error(error)

    } finally {

      setPaying(false)

    }

  }

  if (loading) {
    return (
      <p className="text-white text-center mt-10">
        Chargement...
      </p>
    )
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">

      <div className="max-w-3xl mx-auto">

        <h1 className="text-3xl font-bold mb-6 text-orange-500">
          💳 Paiement
        </h1>

        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">

          <div className="space-y-4">

            {panier.items.map(item => (

              <div
                key={item.id}
                className="flex justify-between border-b border-gray-800 pb-3"
              >

                <div>
                  <h3 className="font-semibold">
                    {item.nom}
                  </h3>

                  <p className="text-sm text-gray-400">
                    x{item.quantite}
                  </p>
                </div>

                <span className="text-orange-500 font-bold">
                  {(item.prix * item.quantite).toFixed(2)} €
                </span>

              </div>

            ))}

          </div>

          <div className="flex justify-between items-center mt-6 text-xl font-bold">

            <span>Total</span>

            <span className="text-orange-500">
              {panier.total} €
            </span>

          </div>

          <div className="flex gap-3 mt-6">

            <button
                onClick={() => navigate("/panier")}
                disabled={paying}
                className="flex-1 border border-gray-700 hover:border-gray-500 py-3 rounded-lg font-bold transition"
            >
                Annuler
            </button>

            <button
                onClick={handlePaiement}
                disabled={paying}
                className="flex-1 bg-orange-500 hover:bg-orange-600 py-3 rounded-lg font-bold transition disabled:opacity-50"
            >

                {paying
                ? "Redirection..."
                : "Payer maintenant"
                }

            </button>

            </div>

        </div>

      </div>

    </div>
  )
}