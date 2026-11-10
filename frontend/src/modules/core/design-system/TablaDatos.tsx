import type { Fila } from "../lib/tipos";
import { formatearCelda } from "../utils/formato";

interface Props {
  columnas: string[];
  filas: Fila[];
  titulo: string;
}

export default function TablaDatos({ columnas, filas, titulo }: Props) {
  if (filas.length === 0) {
    return <p className="estado-carga">La consulta no devolvió filas.</p>;
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
                const texto = formatearCelda(fila[columna] ?? null);
                return (
                  <td key={columna} title={texto}>
                    {texto}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
