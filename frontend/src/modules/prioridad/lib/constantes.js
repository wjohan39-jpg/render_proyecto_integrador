// Relación de simular_prioridades.py: nombre -> nivel -> días máximos de respuesta sugeridos.
export const NIVELES_PRIORIDAD = [
  { nombre: 'Baja', nivel: 1, dias: 12 },
  { nombre: 'Media', nivel: 2, dias: 7 },
  { nombre: 'Alta', nivel: 3, dias: 4 },
]

export const DIAS_MAXIMOS = 90

export const OPCIONES_PRIORIDAD = NIVELES_PRIORIDAD.map((p) => ({ valor: p.nombre, texto: `${p.nombre} (nivel ${p.nivel})` }))

export const COLOR_POR_NOMBRE = { Baja: 'verde', Media: 'amarillo', Alta: 'rojo' }

/** Texto corto de una prioridad para listas desplegables: "Alta · nivel 3 · 4 días · 1a2b3c4d" */
export const describirPrioridad = (p) => `${p.nombre} · nivel ${p.nivel} · ${p.dias_max_respuesta} días · ${p.id.slice(0, 8)}`
