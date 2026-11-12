import Etiqueta from '../../core/design-system/Etiqueta'
import { diasEntre, formatearFecha, humanizar, idCorto } from '../../core/utils/formato'
import { COLOR_ESTADO_RETO } from '../lib/constantes'

// Columnas de la tabla de retos. Recibe los índices { id: item } para mostrar nombres en vez de IDs.
export function crearColumnasReto({ empresasPorId, prioridadesPorId }) {
  return [
    { clave: 'nombre', titulo: 'Reto' },
    { clave: 'estado', titulo: 'Estado', render: (r) => <Etiqueta color={COLOR_ESTADO_RETO[r.estado]}>{humanizar(r.estado)}</Etiqueta> },
    { clave: 'fecha_inicio', titulo: 'Inicio', render: (r) => formatearFecha(r.fecha_inicio) },
    { clave: 'fecha_fin', titulo: 'Fin', render: (r) => formatearFecha(r.fecha_fin) },
    { clave: 'duracion', titulo: 'Días', clase: 'celda-mono', render: (r) => diasEntre(r.fecha_inicio, r.fecha_fin) ?? '—' },
    {
      clave: 'id_empresa',
      titulo: 'Empresa',
      render: (r) => empresasPorId[r.id_empresa]?.nombre ?? <span className="celda-mono celda-tenue">{idCorto(r.id_empresa)}</span>,
    },
    {
      clave: 'id_prioridad',
      titulo: 'Prioridad',
      render: (r) => prioridadesPorId[r.id_prioridad]?.nombre ?? <span className="celda-mono celda-tenue">{idCorto(r.id_prioridad)}</span>,
    },
  ]
}
