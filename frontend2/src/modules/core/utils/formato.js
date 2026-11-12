// Quita espacios sobrantes (equivale a .strip() en Python).
export const limpiar = (texto) => `${texto ?? ''}`.trim()

// Normaliza para comparar sin tildes ni mayúsculas: " LOGÍSTICA " -> "logistica"
export const normalizar = (texto) =>
  limpiar(texto)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')

export const coincide = (texto, busqueda) => normalizar(texto).includes(normalizar(busqueda))

/** "EN_PROGRESO" -> "En progreso" */
export const humanizar = (texto = '') => {
  const t = `${texto}`.replace(/_/g, ' ').toLowerCase()
  return t.charAt(0).toUpperCase() + t.slice(1)
}

/** 1 -> "01" */
export const conCeros = (numero) => String(numero).padStart(2, '0')

/** Primeros 8 caracteres de un UUID, para mostrarlo en tablas. */
export const idCorto = (id) => (id ? `${id}`.slice(0, 8) : '—')

export const iniciales = (nombre = '') =>
  nombre
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0])
    .join('')
    .toUpperCase()

export const plural = (n, singular, pluralTexto) => `${n} ${n === 1 ? singular : pluralTexto}`

const aFecha = (valor) => new Date(`${valor}`.length === 10 ? `${valor}T00:00:00` : `${valor}`.replace(' ', 'T'))

export function formatearFecha(valor) {
  if (!valor) return '—'
  const fecha = aFecha(valor)
  if (Number.isNaN(fecha.getTime())) return `${valor}`
  return fecha.toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' })
}

export function formatearFechaHora(valor) {
  if (!valor) return '—'
  const fecha = aFecha(valor)
  if (Number.isNaN(fecha.getTime())) return `${valor}`
  return fecha.toLocaleString('es-CO', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

/** Días entre dos fechas "AAAA-MM-DD" (puede ser negativo). */
export function diasEntre(inicio, fin) {
  if (!inicio || !fin) return null
  return Math.round((aFecha(fin) - aFecha(inicio)) / 86_400_000)
}

// Sin separador de miles: muchos enteros son identificadores (NIT, teléfono).
const decimales = new Intl.NumberFormat('es-CO', { maximumFractionDigits: 2, useGrouping: false })

/** Texto de una celda de las consultas: nulos, booleanos y números legibles. */
export function formatearCelda(valor) {
  if (valor === null || valor === undefined || valor === '') return '—'
  if (typeof valor === 'boolean') return valor ? 'Sí' : 'No'
  if (typeof valor === 'number') return Number.isInteger(valor) ? String(valor) : decimales.format(valor)
  return `${valor}`
}

/** "2026-07-17 20:59:00" -> formato de <input type="datetime-local"> */
export const aFechaHoraLocal = (valor) => (valor ? `${valor}`.replace(' ', 'T').slice(0, 16) : '')

/** Fecha y hora actuales en formato de <input type="datetime-local">. */
export function ahoraLocal() {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 16)
}
