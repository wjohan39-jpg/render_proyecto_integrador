import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../../auth/hooks/useAuth'
import { INICIO } from '../lib/menu'

// Solo los administradores entran (la API también lo verifica: responde 403).
export default function AdminRoute() {
  const { esAdministrador } = useAuth()
  return esAdministrador ? <Outlet /> : <Navigate to={INICIO} replace />
}
