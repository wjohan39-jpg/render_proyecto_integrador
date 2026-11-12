import { Link } from 'react-router-dom'

// Tarjeta de vidrio con el total de un módulo; lleva a su página.
export default function TarjetaModulo({ titulo, valor, detalle, autor, icono: Icono, ruta }) {
  return (
    <Link to={ruta} className="tarjeta">
      <span className="tarjeta__cabeza">
        <span className="tarjeta__titulo">{titulo}</span>
        <span className="tarjeta__icono" aria-hidden="true">
          <Icono />
        </span>
      </span>
      <span className="tarjeta__valor">{valor}</span>
      <span className="tarjeta__detalle">{detalle}</span>
      <span className="tarjeta__autor">{autor}</span>
    </Link>
  )
}
