import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../../auth/hooks/useAuth'
import EstadoCarga from '../design-system/EstadoCarga'

// Protege las rutas internas: sin sesión, lleva al login y recuerda a dónde quería ir.
export default function PrivateRoute() {
  const { usuario, cargandoSesion } = useAuth()
  const location = useLocation()

  if (cargandoSesion) return <EstadoCarga cargando textoCarga="Validando sesión…" pantalla />
  if (!usuario) return <Navigate to="/login" replace state={{ desde: location.pathname + location.search }} />
  return <Outlet />
}
