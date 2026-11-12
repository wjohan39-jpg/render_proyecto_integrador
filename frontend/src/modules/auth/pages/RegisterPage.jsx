import AuthLayout from '../components/AuthLayout'
import RegisterForm from '../components/RegisterForm'

export default function RegisterPage() {
  return (
    <AuthLayout titulo="Crear cuenta" subtitulo="Regístrate para gestionar empresas, prioridades, retos y registros.">
      <RegisterForm />
    </AuthLayout>
  )
}
