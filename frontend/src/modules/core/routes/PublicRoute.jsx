import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../../auth/hooks/useAuth'
import EstadoCarga from '../design-system/EstadoCarga'
import { INICIO } from '../lib/menu'

// Login y Registro: con sesión activa no tiene sentido verlos; se va al panel.
export default function PublicRoute() {
  const { usuario, cargandoSesion } = useAuth()
  const location = useLocation()

  if (cargandoSesion) return <EstadoCarga cargando textoCarga="Validando sesión…" pantalla />
  if (usuario) return <Navigate to={location.state?.desde ?? INICIO} replace />
  return <Outlet />
}
