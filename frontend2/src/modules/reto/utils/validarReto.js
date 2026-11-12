import { esVacio } from '../../core/utils/validaciones'
import { limpiar } from '../../core/utils/formato'

export function validarReto(valores) {
  const fechasCompletas = valores.fecha_inicio && valores.fecha_fin
  return {
    nombre: limpiar(valores.nombre).length < 3 ? 'El nombre debe tener al menos 3 caracteres.' : undefined,
    descripcion: limpiar(valores.descripcion).length < 3 ? 'Escribe una descripción.' : undefined,
    fecha_inicio: !valores.fecha_inicio ? 'Elige la fecha de inicio.' : undefined,
    fecha_fin: !valores.fecha_fin
      ? 'Elige la fecha de fin.'
      : fechasCompletas && valores.fecha_fin < valores.fecha_inicio
        ? 'La fecha de fin no puede ser anterior a la de inicio.'
        : undefined,
    estado: esVacio(valores.estado) ? 'Selecciona un estado.' : undefined,
  }
}

const opcional = (valor) => limpiar(valor) || null

export function normalizarReto(valores) {
  return {
    nombre: limpiar(valores.nombre),
    descripcion: limpiar(valores.descripcion),
    fecha_inicio: valores.fecha_inicio,
    fecha_fin: valores.fecha_fin,
    estado: valores.estado,
    id_empresa: opcional(valores.id_empresa),
    id_prioridad: opcional(valores.id_prioridad),
    id_categoria: opcional(valores.id_categoria),
  }
}
