import { esVacio } from '../../core/utils/validaciones'
import { limpiar } from '../../core/utils/formato'

export function validarRegistro(valores) {
  return {
    fecha_registro: !valores.fecha_registro ? 'Elige la fecha y hora del registro.' : undefined,
    estado: esVacio(valores.estado) ? 'Selecciona un estado.' : undefined,
    observacion: esVacio(valores.observacion) ? 'Escribe una observación.' : undefined,
  }
}

const opcional = (valor) => limpiar(valor) || null

export function normalizarRegistro(valores) {
  return {
    fecha_registro: valores.fecha_registro,
    estado: valores.estado,
    observacion: limpiar(valores.observacion),
    id_reto: opcional(valores.id_reto),
    id_usuario: opcional(valores.id_usuario),
  }
}
