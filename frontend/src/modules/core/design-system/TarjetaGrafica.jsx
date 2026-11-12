import { urlApi } from '../lib/apiClient'
import { conCeros } from '../utils/formato'

// Tarjeta de una gráfica PNG generada por main.py (se abre en grande al hacer clic).
export default function TarjetaGrafica({ grafica }) {
  const ruta = urlApi(grafica.url)
  return (
    <article className="grafica">
      <header className="grafica__encabezado">
        <span className="grafica__numero">{conCeros(grafica.numero)}</span>
        <div>
          <h2>{grafica.titulo}</h2>
          <p>{grafica.descripcion}</p>
        </div>
      </header>
      <a className="grafica__imagen-enlace" href={ruta} target="_blank" rel="noreferrer" aria-label={`Abrir gráfica: ${grafica.titulo}`}>
        <img src={ruta} alt={grafica.alt} loading="lazy" />
      </a>
    </article>
  )
}
