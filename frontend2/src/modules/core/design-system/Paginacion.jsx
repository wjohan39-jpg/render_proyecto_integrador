import Boton from './Boton'

// Anterior · Página X de Y · Siguiente, con el total de filas a la izquierda.
export default function Paginacion({ pagina, totalPaginas, total, onCambiar }) {
  return (
    <div className="paginacion">
      <span className="panel__nota">{total === 1 ? '1 fila' : `${total} filas`}</span>
      <div className="panel__acciones">
        <Boton onClick={() => onCambiar(pagina - 1)} disabled={pagina <= 1}>
          Anterior
        </Boton>
        <span className="panel__pagina">
          Página {pagina} de {totalPaginas}
        </span>
        <Boton onClick={() => onCambiar(pagina + 1)} disabled={pagina >= totalPaginas}>
          Siguiente
        </Boton>
      </div>
    </div>
  )
}
