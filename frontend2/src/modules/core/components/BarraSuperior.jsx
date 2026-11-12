import { Link } from 'react-router-dom'
import { LogOut } from 'lucide-react'
import Boton from '../design-system/Boton'
import { iniciales } from '../utils/formato'
import { INICIO } from '../lib/menu'

// Marca "PI · PROYECTO INTEGRADOR CESDE" y, con sesión, el usuario y el botón Salir.
export default function BarraSuperior({ usuario, onSalir }) {
  return (
    <header className="barra-superior">
      <Link className="marca" to={usuario ? INICIO : '/login'} aria-label="Proyecto Integrador Cesde, inicio">
        <span className="marca__sello" aria-hidden="true">
          PI
        </span>
        <span className="marca__nombre">
          PROYECTO INTEGRADOR <strong>CESDE</strong>
        </span>
      </Link>

      <div className="barra-superior__derecha">
        <span className="estado">
          <span className="estado__punto" />
          Conectado a la API
        </span>
        {usuario && (
          <>
            <span className="sesion">
              <span className="sesion__avatar" aria-hidden="true">
                {iniciales(usuario.nombre)}
              </span>
              <span className="sesion__datos">
                <span className="sesion__nombre">{usuario.nombre}</span>
                <span className="sesion__rol">{usuario.rol}</span>
              </span>
            </span>
            <Boton icono={LogOut} onClick={onSalir}>
              Salir
            </Boton>
          </>
        )}
      </div>
    </header>
  )
}
