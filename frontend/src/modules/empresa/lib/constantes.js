// Mismos sectores de simular_empresas.py y de la API (api/esquemas.py)
export const SECTORES = ['Tecnologia', 'Salud', 'Manufactura', 'Energia']

export const OPCIONES_SECTOR = SECTORES.map((s) => ({ valor: s, texto: s }))

export const OPCIONES_ESTADO = [
  { valor: 'activas', texto: 'Activas' },
  { valor: 'inactivas', texto: 'Inactivas' },
]
