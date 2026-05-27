import { createBrowserRouter } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Menu from './pages/Menu'
import Panier from './pages/Panier'
import Commandes from './pages/Commandes'

export const router = createBrowserRouter([
  { path: '/',          element: <Login /> },
  { path: '/register',  element: <Register /> },
  { path: '/menu',      element: <Menu /> },
  { path: '/panier',    element: <Panier /> },
  { path: '/commandes', element: <Commandes /> },
])