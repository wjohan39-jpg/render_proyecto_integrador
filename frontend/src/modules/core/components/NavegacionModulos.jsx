import { NavLink } from 'react-router-dom'

// Pestañas de los módulos (mismo diseño que la navegación del visor).
export default function NavegacionModulos({ opciones }) {
  return (
    <nav className="navegacion" aria-label="Módulos del proyecto">
      {opciones.map(({ ruta, texto, detalle, icono: Icono }) => (
        <NavLink key={ruta} to={ruta} className="pestana">
          <span className="pestana__titulo">
            <Icono aria-hidden="true" />
            {texto}
          </span>
          <span className="pestana__detalle">{detalle}</span>
        </NavLink>
      ))}
    </nav>
  )
}
