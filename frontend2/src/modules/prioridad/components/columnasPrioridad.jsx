import Etiqueta from '../../core/design-system/Etiqueta'
import { idCorto } from '../../core/utils/formato'
import { COLOR_POR_NOMBRE } from '../lib/constantes'

// Columnas de la tabla de prioridades.
export const COLUMNAS_PRIORIDAD = [
  { clave: 'nombre', titulo: 'Prioridad', render: (p) => <Etiqueta color={COLOR_POR_NOMBRE[p.nombre]}>{p.nombre}</Etiqueta> },
  { clave: 'nivel', titulo: 'Nivel', clase: 'celda-mono' },
  { clave: 'dias_max_respuesta', titulo: 'Días máx. de respuesta', clase: 'celda-mono' },
  { clave: 'id', titulo: 'ID', clase: 'celda-mono celda-tenue', render: (p) => idCorto(p.id) },
]
