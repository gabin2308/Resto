import { createBrowserRouter } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Menu from './pages/Menu'
import Panier from './pages/Panier'
import Commandes from './pages/Commandes'
import Paiement from "./pages/Paiement"
import PaiementSuccess from "./pages/PaiementSuccess"
import PaiementCancel from "./pages/PaiementCancel"
import Historique from "./pages/Historique"
import Gestionnaire from "./pages/Gestionnaire"

export const router = createBrowserRouter([
  { path: '/',          element: <Login /> },
  { path: '/register',  element: <Register /> },
  { path: '/menu',      element: <Menu /> },
  { path: '/panier',    element: <Panier /> },
  { path: '/commandes', element: <Commandes /> },
  { path: '/paiement',  element: <Paiement /> },
  { path: '/paiement/success', element: <PaiementSuccess /> },
  { path: '/paiement/cancel', element: <PaiementCancel /> },
  { path: '/historique', element: <Historique /> },
  { path: '/gestionnaire', element: <Gestionnaire /> }
])