import { useState } from 'react'
import { Plus, Search } from 'lucide-react'
import Boton from '../design-system/Boton'
import Modal from '../design-system/Modal'
import Confirmacion from '../design-system/Confirmacion'
import Aviso from '../design-system/Aviso'
import EstadoCarga from '../design-system/EstadoCarga'
import TablaCrud from '../design-system/TablaCrud'
import Paginacion from '../design-system/Paginacion'
import { useTablaFiltrada } from '../hooks/useTablaFiltrada'

// Panel CRUD reutilizado por todos los módulos:
// buscar + filtros + "Nuevo" -> tabla paginada -> modal con el formulario -> confirmación al eliminar.
//
// crud:        resultado de useCrud (items, cargando, error, crear, actualizar, eliminar, recargar)
// entidad:     { singular: 'empresa', articulo: 'la' }   -> textos de los mensajes
// columnas:    columnas de TablaCrud
// buscarEn:    (item) => [textos donde buscar]
// filtros:     [{ clave, etiqueta, opciones: [{ valor, texto }], aplicar(item, valor) }]
// Formulario:  componente con props { item, onGuardar, onCancelar, ...propsFormulario }
// describir:   (item) => nombre corto para los mensajes
// validarEliminar: (item) => texto de error si no se puede eliminar (opcional)
export default function GestionCrud({
  crud,
  entidad,
  columnas,
  buscarEn,
  filtros = [],
  Formulario,
  propsFormulario = {},
  describir,
  validarEliminar,
}) {
  const { items, cargando, error, recargar, crear, actualizar, eliminar } = crud
  const tabla = useTablaFiltrada(items, { buscarEn, filtros })
  const [enEdicion, setEnEdicion] = useState(null) // null = cerrado, {} = nuevo, item = editar
  const [porEliminar, setPorEliminar] = useState(null)
  const [aviso, setAviso] = useState(null)

  const { singular, articulo } = entidad
  const nuevo = articulo === 'la' ? 'nueva' : 'nuevo'
  const Singular = singular.charAt(0).toUpperCase() + singular.slice(1)
  const terminacion = articulo === 'la' ? 'a' : 'o'

  const guardar = async (datos) => {
    if (enEdicion.id) {
      const guardado = await actualizar(enEdicion.id, datos)
      setAviso({ tipo: 'exito', texto: `${Singular} "${describir(guardado)}" actualizad${terminacion}.` })
    } else {
      const guardado = await crear(datos)
      setAviso({ tipo: 'exito', texto: `${Singular} "${describir(guardado)}" cread${terminacion}.` })
    }
    setEnEdicion(null)
  }

  const pedirEliminar = (item) => {
    const problema = validarEliminar?.(item)
    if (problema) {
      setAviso({ tipo: 'error', texto: problema })
      return
    }
    setPorEliminar(item)
  }

  const confirmarEliminar = async () => {
    const item = porEliminar
    try {
      await eliminar(item.id)
      setAviso({ tipo: 'exito', texto: `${Singular} "${describir(item)}" eliminad${terminacion}.` })
    } catch (fallo) {
      setAviso({ tipo: 'error', texto: fallo.message })
    } finally {
      setPorEliminar(null)
    }
  }

  return (
    <section className="panel" aria-label={`Gestión de ${singular}`}>
      <div className="herramientas">
        <label className="buscador">
          <span className="sr-only">Buscar</span>
          <Search aria-hidden="true" />
          <input
            type="search"
            className="control"
            placeholder="Buscar…"
            value={tabla.busqueda}
            onChange={(e) => tabla.setBusqueda(e.target.value)}
          />
        </label>
        {filtros.map((f) => (
          <label key={f.clave} className="filtro">
            <span className="sr-only">{f.etiqueta}</span>
            <select className="control" value={tabla.valores[f.clave] ?? ''} onChange={(e) => tabla.cambiarFiltro(f.clave, e.target.value)}>
              <option value="">{f.etiqueta}: todos</option>
              {f.opciones.map((op) => (
                <option key={op.valor} value={op.valor}>
                  {op.texto}
                </option>
              ))}
            </select>
          </label>
        ))}
        <span className="herramientas__espacio" />
        <Boton variante="primario" icono={Plus} onClick={() => setEnEdicion({})}>
          {`${nuevo.charAt(0).toUpperCase()}${nuevo.slice(1)} ${singular}`}
        </Boton>
      </div>

      {aviso && (
        <Aviso tipo={aviso.tipo} onCerrar={() => setAviso(null)}>
          {aviso.texto}
        </Aviso>
      )}

      {cargando || error ? (
        <EstadoCarga cargando={cargando} error={error} onReintentar={recargar} />
      ) : (
        <>
          <TablaCrud
            columnas={columnas}
            filas={tabla.visibles}
            titulo={`Tabla de ${singular}`}
            describir={describir}
            onEditar={setEnEdicion}
            onEliminar={pedirEliminar}
            vacio={items.length ? 'Ningún elemento coincide con la búsqueda o los filtros.' : 'Aún no hay datos. Crea el primero con el botón de arriba.'}
          />
          <Paginacion pagina={tabla.pagina} totalPaginas={tabla.totalPaginas} total={tabla.total} onCambiar={tabla.setPagina} />
        </>
      )}

      <Modal abierto={enEdicion !== null} titulo={enEdicion?.id ? `Editar ${singular}` : `${Singular} ${nuevo}`} onCerrar={() => setEnEdicion(null)}>
        {enEdicion && <Formulario item={enEdicion} onGuardar={guardar} onCancelar={() => setEnEdicion(null)} {...propsFormulario} />}
      </Modal>

      <Confirmacion
        abierto={porEliminar !== null}
        titulo={`¿Eliminar ${articulo} ${singular}?`}
        mensaje={porEliminar ? `Se eliminará "${describir(porEliminar)}". Esta acción no se puede deshacer.` : ''}
        onConfirmar={confirmarEliminar}
        onCancelar={() => setPorEliminar(null)}
      />
    </section>
  )
}
