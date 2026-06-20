import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { authService } from "../services/authService"
import { useAuth } from "../context/AuthContext"


export default function Login() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError]       = useState("")
  const navigate                = useNavigate()
  const {login} = useAuth()

  const handleLogin = async () => {
    if (!username || !password) {
      setError("Remplis tous les champs")
      return
    }

    const data = await authService.login(username, password)

    if (data.success) {
      login(data.user)
      navigate('/menu')
    } else {
      setError(data.error)
    }
  }

  return (
  <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
    <div className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-2xl p-8 flex flex-col gap-4">
      
      <div className="flex justify-center mb-2">
        <img src="/resto_logo.svg" alt="Resto" className="h-26" />
      </div>
      <h2 className="text-xl font-semibold text-white">Connexion</h2>

      {error && (
        <p className="text-red-400 text-sm bg-red-950 border border-red-800 px-4 py-2 rounded-lg">
          {error}
        </p>
      )}

      <input
        type="text"
        placeholder="Nom d'utilisateur"
        value={username}
        onChange={e => setUsername(e.target.value)}
        className="bg-gray-950 border border-gray-700 text-white px-4 py-3 rounded-lg outline-none focus:border-orange-500 transition"
      />
      <input
        type="password"
        placeholder="Mot de passe"
        value={password}
        onChange={e => setPassword(e.target.value)}
        className="bg-gray-950 border border-gray-700 text-white px-4 py-3 rounded-lg outline-none focus:border-orange-500 transition"
      />

      <button
        onClick={handleLogin}
        className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg transition"
      >
        Se connecter
      </button>

      <p className="text-gray-400 text-sm text-center">
        Pas de compte ?{" "}
        <Link to="/register" className="text-orange-500 hover:underline">
          S'inscrire
        </Link>
      </p>

    </div>
  </div>
)  }