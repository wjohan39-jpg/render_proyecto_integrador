import { api, guardarToken, limpiarToken, obtenerToken } from '../../core/lib/apiClient'
import { borrar, guardar, leer } from '../../core/lib/storage'

// Endpoints de la API: POST /api/auth/login, POST /api/auth/register, GET /api/auth/me, POST /api/auth/logout
const CLAVE_USUARIO = 'usuario'

export function obtenerSesion() {
  return obtenerToken() ? leer(CLAVE_USUARIO) : null
}

function abrirSesion({ token, usuario }) {
  guardarToken(token)
  guardar(CLAVE_USUARIO, usuario)
  return usuario
}

export async function iniciarSesion(correo, contrasena) {
  const datos = await api.post('/api/auth/login', { correo: correo.trim().toLowerCase(), contrasena }, { auth: false })
  return abrirSesion(datos)
}

export async function registrar({ nombre, correo, contrasena, rol }) {
  const datos = await api.post(
    '/api/auth/register',
    { nombre: nombre.trim(), correo: correo.trim().toLowerCase(), contrasena, rol },
    { auth: false },
  )
  return abrirSesion(datos)
}

// Al recargar la página se valida el token guardado contra la API.
export async function restaurarSesion() {
  if (!obtenerToken()) {
    borrar(CLAVE_USUARIO)
    return null
  }
  try {
    const usuario = await api.get('/api/auth/me')
    guardar(CLAVE_USUARIO, usuario)
    return usuario
  } catch {
    olvidarSesion()
    return null
  }
}

// Borra la sesión en la API (si se puede) y en el navegador.
export async function cerrarSesion() {
  if (obtenerToken()) {
    await api.post('/api/auth/logout', undefined, { auth: true }).catch(() => null)
  }
  olvidarSesion()
}

export function olvidarSesion() {
  limpiarToken()
  borrar(CLAVE_USUARIO)
}
