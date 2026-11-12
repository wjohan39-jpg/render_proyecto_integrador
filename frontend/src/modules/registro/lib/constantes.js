import { humanizar } from '../../core/utils/formato'

// Estados que existen en registros_limpio.csv y que acepta la API (api/esquemas.py)
export const ESTADOS_REGISTRO = ['INSCRITO', 'EN_PROCESO', 'FINALIZADO']

export const OPCIONES_ESTADO_REGISTRO = ESTADOS_REGISTRO.map((e) => ({ valor: e, texto: humanizar(e) }))

export const COLOR_ESTADO_REGISTRO = {
  INSCRITO: 'amarillo',
  EN_PROCESO: 'magenta',
  FINALIZADO: 'verde',
}
