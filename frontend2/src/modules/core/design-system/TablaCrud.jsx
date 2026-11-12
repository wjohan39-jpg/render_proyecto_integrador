import { Pencil, Trash2 } from 'lucide-react'
import BotonIcono from './BotonIcono'

// Tabla de un módulo CRUD con las acciones Editar / Eliminar en cada fila.
// columnas: [{ clave, titulo, render?(item), clase?, titulo?(item) }]
export default function TablaCrud({ columnas, filas, titulo, describir, onEditar, onEliminar, vacio = 'No hay datos para mostrar.' }) {
  if (filas.length === 0) {
    return <p className="estado-carga">{vacio}</p>
  }

  return (
    <div className="tabla" role="region" aria-label={titulo} tabIndex={0}>
      <table>
        <thead>
          <tr>
            {columnas.map((c) => (
              <th key={c.clave} scope="col">
                {c.titulo}
              </th>
            ))}
            <th scope="col" className="celda-acciones">
              <span className="sr-only">Acciones</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {filas.map((item) => (
            <tr key={item.id}>
              {columnas.map((c) => {
                const valor = c.render ? c.render(item) : (item[c.clave] ?? '—')
                const texto = typeof valor === 'string' || typeof valor === 'number' ? String(valor) : undefined
                return (
                  <td key={c.clave} className={c.clase} title={texto}>
                    {valor}
                  </td>
                )
              })}
              <td className="celda-acciones">
                <BotonIcono icono={Pencil} etiqueta={`Editar ${describir(item)}`} onClick={() => onEditar(item)} />
                <BotonIcono icono={Trash2} etiqueta={`Eliminar ${describir(item)}`} peligro onClick={() => onEliminar(item)} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
