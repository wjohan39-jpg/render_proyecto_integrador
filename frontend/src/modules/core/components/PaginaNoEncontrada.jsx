import { Link } from 'react-router-dom'
import FondoAnimado from './FondoAnimado'
import BarraSuperior from './BarraSuperior'
import { INICIO } from '../lib/menu'

export default function PaginaNoEncontrada() {
  return (
    <>
      <FondoAnimado />
      <div className="pagina">
        <BarraSuperior />
        <main className="no-encontrada">
          <p className="sobretitulo">ERROR 404</p>
          <h1>
            Página no encontrada<span>.</span>
          </h1>
          <p>La dirección que buscas no existe.</p>
          <Link to={INICIO} className="boton boton--primario boton--grande">
            Volver al inicio
          </Link>
        </main>
      </div>
    </>
  )
}
