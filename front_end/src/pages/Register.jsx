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
    <div className="auth-page">
      <h1>🍔 Resto</h1>
      <div className="auth-form">
        <h2>Inscription</h2>

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
        <input
          type="password"
          placeholder="Confirmer le mot de passe"
          value={confirm}
          onChange={e => setConfirm(e.target.value)}
        />

        <button onClick={handleRegister}>S'inscrire</button>

        <p>Déjà un compte ? <Link to="/">Se connecter</Link></p>
      </div>
    </div>
  )
}