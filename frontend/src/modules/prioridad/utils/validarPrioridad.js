import { esVacio } from '../../core/utils/validaciones'
import { DIAS_MAXIMOS, NIVELES_PRIORIDAD } from '../lib/constantes'

export function validarPrioridad(valores) {
  const dias = Number(valores.dias_max_respuesta)
  return {
    nombre: esVacio(valores.nombre) ? 'Selecciona la prioridad.' : undefined,
    dias_max_respuesta:
      !Number.isInteger(dias) || dias < 1 || dias > DIAS_MAXIMOS ? `Escribe un número entero entre 1 y ${DIAS_MAXIMOS}.` : undefined,
  }
}

// El nivel se deduce del nombre para que siempre coincidan (la API también lo exige).
export function normalizarPrioridad(valores) {
  const nivel = NIVELES_PRIORIDAD.find((p) => p.nombre === valores.nombre)?.nivel
  return {
    nombre: valores.nombre,
    nivel,
    dias_max_respuesta: Number(valores.dias_max_respuesta),
  }
}
