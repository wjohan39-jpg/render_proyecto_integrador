import AuthLayout from '../components/AuthLayout'
import LoginForm from '../components/LoginForm'

export default function LoginPage() {
  return (
    <AuthLayout titulo="Iniciar sesión" subtitulo="Ingresa tus datos para entrar al panel.">
      <LoginForm />
    </AuthLayout>
  )
}
