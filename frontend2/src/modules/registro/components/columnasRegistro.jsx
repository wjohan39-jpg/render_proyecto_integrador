import Etiqueta from '../../core/design-system/Etiqueta'
import { formatearFechaHora, humanizar, idCorto } from '../../core/utils/formato'
import { COLOR_ESTADO_REGISTRO } from '../lib/constantes'

const idTenue = (id) => <span className="celda-mono celda-tenue">{idCorto(id)}</span>

// Columnas de la tabla de registros. Recibe los índices { id: item } para mostrar nombres en vez de IDs.
export function crearColumnasRegistro({ retosPorId, usuariosPorId }) {
  return [
    { clave: 'fecha_registro', titulo: 'Fecha', render: (r) => formatearFechaHora(r.fecha_registro) },
    {
      clave: 'estado',
      titulo: 'Estado',
      render: (r) => <Etiqueta color={COLOR_ESTADO_REGISTRO[r.estado]}>{humanizar(r.estado)}</Etiqueta>,
    },
    { clave: 'id_reto', titulo: 'Reto', render: (r) => retosPorId[r.id_reto]?.nombre ?? idTenue(r.id_reto) },
    { clave: 'id_usuario', titulo: 'Usuario', render: (r) => usuariosPorId[r.id_usuario]?.nombre ?? idTenue(r.id_usuario) },
    { clave: 'observacion', titulo: 'Observación' },
  ]
}
