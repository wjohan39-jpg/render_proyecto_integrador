import { Link, useLocation, useNavigate } from 'react-router-dom'
import { LogIn } from 'lucide-react'
import { useFormulario } from '../../core/hooks/useFormulario'
import Input from '../../core/design-system/Input'
import Boton from '../../core/design-system/Boton'
import Aviso from '../../core/design-system/Aviso'
import { INICIO } from '../../core/lib/menu'
import { useAuth } from '../hooks/useAuth'
import { validarLogin } from '../utils/validarAuth'

export default function LoginForm() {
  const { iniciarSesion } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  // Si venía de una ruta privada, volver a ella después de entrar
  const destino = location.state?.desde ?? INICIO

  const { valores, errores, enviando, cambiar, enviar } = useFormulario({ correo: '', contrasena: '' }, validarLogin, async ({ correo, contrasena }) => {
    await iniciarSesion(correo, contrasena)
    navigate(destino, { replace: true })
  })

  return (
    <form className="formulario" onSubmit={enviar} noValidate>
      {errores.general && <Aviso>{errores.general}</Aviso>}

      <Input
        name="correo"
        type="email"
        etiqueta="Correo electrónico"
        placeholder="tucorreo@ejemplo.com"
        autoComplete="email"
        value={valores.correo}
        onChange={cambiar}
        error={errores.correo}
      />
      <Input
        name="contrasena"
        type="password"
        etiqueta="Contraseña"
        placeholder="••••••••"
        autoComplete="current-password"
        value={valores.contrasena}
        onChange={cambiar}
        error={errores.contrasena}
      />

      <Boton type="submit" variante="primario" grande bloque icono={LogIn} disabled={enviando}>
        {enviando ? 'Ingresando…' : 'Iniciar sesión'}
      </Boton>

      <p className="acceso__pie">
        ¿No tienes cuenta?{' '}
        <Link to="/registro" className="enlace">
          Regístrate
        </Link>
      </p>

      <div className="acceso__prueba">
        <strong>USUARIO DE PRUEBA</strong>
        admin@cesde.edu.co · Admin123*
      </div>
    </form>
  )
}
