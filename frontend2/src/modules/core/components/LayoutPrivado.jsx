import { Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../../auth/hooks/useAuth'
import { PESTANAS } from '../lib/menu'
import BarraSuperior from './BarraSuperior'
import FondoAnimado from './FondoAnimado'
import NavegacionModulos from './NavegacionModulos'
import PiePagina from './PiePagina'

// Estructura de las páginas con sesión: fondo animado, barra superior, pestañas y contenido.
export default function LayoutPrivado() {
  const { usuario, esAdministrador, cerrarSesion } = useAuth()
  const navigate = useNavigate()
  const pestanas = PESTANAS.filter((p) => !p.soloAdmin || esAdministrador)

  const salir = async () => {
    await cerrarSesion()
    navigate('/login', { replace: true })
  }

  return (
    <>
      <FondoAnimado />
      <div className="pagina">
        <BarraSuperior usuario={usuario} onSalir={salir} />
        <NavegacionModulos opciones={pestanas} />
        <main className="pagina__contenido">
          <Outlet />
        </main>
        <PiePagina />
      </div>
    </>
  )
}
