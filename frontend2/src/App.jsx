import { Navigate, Route, Routes } from 'react-router-dom'
import PrivateRoute from './modules/core/routes/PrivateRoute'
import PublicRoute from './modules/core/routes/PublicRoute'
import AdminRoute from './modules/core/routes/AdminRoute'
import LayoutPrivado from './modules/core/components/LayoutPrivado'
import PaginaNoEncontrada from './modules/core/components/PaginaNoEncontrada'
import { INICIO } from './modules/core/lib/menu'
import LoginPage from './modules/auth/pages/LoginPage'
import RegisterPage from './modules/auth/pages/RegisterPage'
import DashboardPage from './modules/dashboard/pages/DashboardPage'
import EmpresasPage from './modules/empresa/pages/EmpresasPage'
import PrioridadesPage from './modules/prioridad/pages/PrioridadesPage'
import RetosPage from './modules/reto/pages/RetosPage'
import RegistrosPage from './modules/registro/pages/RegistrosPage'
import UsuariosPage from './modules/usuario/pages/UsuariosPage'

export default function App() {
  return (
    <Routes>
      {/* Rutas públicas: con sesión activa redirigen al panel */}
      <Route element={<PublicRoute />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/registro" element={<RegisterPage />} />
      </Route>

      {/* Rutas privadas: sin sesión redirigen al login */}
      <Route element={<PrivateRoute />}>
        <Route element={<LayoutPrivado />}>
          <Route path={INICIO} element={<DashboardPage />} />
          <Route path="/empresas" element={<EmpresasPage />} />
          <Route path="/prioridades" element={<PrioridadesPage />} />
          <Route path="/retos" element={<RetosPage />} />
          <Route path="/registros" element={<RegistrosPage />} />
          <Route element={<AdminRoute />}>
            <Route path="/usuarios" element={<UsuariosPage />} />
          </Route>
        </Route>
      </Route>

      <Route path="/" element={<Navigate to={INICIO} replace />} />
      <Route path="*" element={<PaginaNoEncontrada />} />
    </Routes>
  )
}
