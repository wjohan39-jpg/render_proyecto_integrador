import { formatearCelda } from '../utils/formato'

// Tabla genérica para las consultas de los reportes (columnas dinámicas).
export default function TablaDatos({ columnas, filas, titulo }) {
  if (filas.length === 0) {
    return <p className="estado-carga">La consulta no devolvió filas.</p>
  }
  return (
    <div className="tabla" role="region" aria-label={titulo} tabIndex={0}>
      <table>
        <thead>
          <tr>
            {columnas.map((columna) => (
              <th key={columna} scope="col">
                {columna}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filas.map((fila, indice) => (
            <tr key={indice}>
              {columnas.map((columna) => {
                const texto = formatearCelda(fila[columna])
                return (
                  <td key={columna} title={texto}>
                    {texto}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
