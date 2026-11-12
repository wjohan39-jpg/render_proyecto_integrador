import { idCorto } from './formato'

/**
 * Opciones de un <select> que apunta a otra tabla (empresa, prioridad, reto…).
 * Si el valor guardado no existe en la lista (datos simulados con IDs sin relación),
 * se agrega para no perderlo al editar.
 */
export function opcionesRelacion(items, describir, valorActual) {
  const opciones = items.map((item) => ({ valor: item.id, texto: describir(item) }))
  if (valorActual && !items.some((item) => item.id === valorActual)) {
    opciones.unshift({ valor: valorActual, texto: `ID ${idCorto(valorActual)} (sin coincidencia)` })
  }
  return opciones
}

/** { id: item } para buscar rápido el nombre de una relación. */
export const indexarPorId = (items) => Object.fromEntries(items.map((item) => [item.id, item]))
