import { humanizar } from '../../core/utils/formato'

// Panel con barras horizontales simples: una por categoría, proporcional al máximo.
// conteo: { categoria: cantidad }
export default function PanelBarras({ titulo, conclusion, conteo }) {
  const filas = Object.entries(conteo).sort((a, b) => b[1] - a[1])
  const maximo = Math.max(1, ...filas.map(([, n]) => n))

  return (
    <section className="panel" aria-label={titulo}>
      <h2>{titulo}</h2>
      {conclusion && <p className="panel__subtitulo">{conclusion}</p>}
      <ul className="barras">
        {filas.map(([nombre, total]) => (
          <li key={nombre}>
            <div className="barras__fila">
              <span>{humanizar(nombre)}</span>
              <strong>{total}</strong>
            </div>
            <div className="barras__pista">
              <div className="barras__relleno" style={{ width: `${(total / maximo) * 100}%` }} />
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}
