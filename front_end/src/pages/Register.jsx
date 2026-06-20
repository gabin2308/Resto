import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { authService } from "../services/authService"

export default function Register() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirm,  setConfirm]  = useState("")
  const [error,    setError]    = useState("")
  const navigate                = useNavigate()

  const handleRegister = async () => {
    if (!username || !password || !confirm) {
      setError("Remplis tous les champs")
      return
    }
    if (password !== confirm) {
      setError("Les mots de passe ne correspondent pas")
      return
    }
    if (password.length < 6) {
      setError("Le mot de passe doit faire au moins 6 caractères")
      return
    }

    const data = await authService.register(username, password)
    if (data.success) {
      navigate('/menu')
    } else {
      setError(data.error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-2xl p-8 flex flex-col gap-4">

        <h1 className="text-3xl font-bold text-orange-500 text-center">🍔 Resto</h1>
        <h2 className="text-xl font-semibold text-white">Inscription</h2>

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
        <input
          type="password"
          placeholder="Confirmer le mot de passe"
          value={confirm}
          onChange={e => setConfirm(e.target.value)}
          className="bg-gray-950 border border-gray-700 text-white px-4 py-3 rounded-lg outline-none focus:border-orange-500 transition"
        />

        <button
          onClick={handleRegister}
          className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg transition"
        >
          S'inscrire
        </button>

        <p className="text-gray-400 text-sm text-center">
          Déjà un compte ?{" "}
          <Link to="/" className="text-orange-500 hover:underline">
            Se connecter
          </Link>
        </p>

      </div>
    </div>
  )
}