// Mismos roles que acepta la API (api/esquemas.py)
export const ROLES = ['administrador', 'empresario', 'profesor']

// El registro público no puede crear administradores (los crea otro administrador en Usuarios).
export const ROLES_REGISTRO = ['empresario', 'profesor']

export const opcionesRol = (roles) => roles.map((rol) => ({ valor: rol, texto: rol.charAt(0).toUpperCase() + rol.slice(1) }))
