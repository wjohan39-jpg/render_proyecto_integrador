import { humanizar } from '../../core/utils/formato'

// Estados que existen en retos_limpio.csv y que acepta la API (api/esquemas.py)
export const ESTADOS_RETO = ['PENDIENTE', 'EN_PROGRESO', 'EN_CURSO', 'COMPLETADA', 'CERRADO']

export const OPCIONES_ESTADO_RETO = ESTADOS_RETO.map((e) => ({ valor: e, texto: humanizar(e) }))

export const COLOR_ESTADO_RETO = {
  PENDIENTE: 'amarillo',
  EN_PROGRESO: 'magenta',
  EN_CURSO: 'morado',
  COMPLETADA: 'verde',
  CERRADO: 'gris',
}
