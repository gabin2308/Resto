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
    <div className="auth-page">
      <h1>🍔 Resto</h1>
      <div className="auth-form">
        <h2>Connexion</h2>

        {error && <p className="error">{error}</p>}

        <input
          type="text"
          placeholder="Nom d'utilisateur"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Mot de passe"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Se connecter</button>

        <p>Pas de compte ? <Link to="/register">S'inscrire</Link></p>
      </div>
    </div>
  )
}