import { opcionesRol, ROLES } from '../../auth/lib/constantes'

// Un administrador puede asignar cualquiera de los roles que acepta la API.
export const OPCIONES_ROL = opcionesRol(ROLES)

export const OPCIONES_ESTADO = [
  { valor: 'activos', texto: 'Activos' },
  { valor: 'inactivos', texto: 'Inactivos' },
]

export const COLOR_ROL = { administrador: 'magenta', empresario: 'morado', profesor: 'naranja' }
