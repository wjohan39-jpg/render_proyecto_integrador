// Cliente HTTP de la API FastAPI (carpeta api/ del proyecto).
// - En desarrollo VITE_API_URL queda vacío y Vite reenvía /api a http://127.0.0.1:8000.
// - En producción VITE_API_URL es la URL de la API (por ejemplo la de Render).

export const API_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')
export const EVENTO_SESION_EXPIRADA = 'sesion-expirada'
const CLAVE_TOKEN = 'token'

export class ApiError extends Error {
  constructor(mensaje, estado = 0, campos = {}) {
    super(mensaje)
    this.name = 'ApiError'
    this.estado = estado
    this.campos = campos
  }
}

/** Convierte una ruta de la API (/api/...) en URL completa. */
export const urlApi = (ruta) => `${API_URL}${ruta}`

export function obtenerToken() {
  try {
    return localStorage.getItem(CLAVE_TOKEN)
  } catch {
    return null
  }
}

export function guardarToken(token) {
  try {
    localStorage.setItem(CLAVE_TOKEN, token)
  } catch {
    // localStorage bloqueado: la sesión no sobrevive a una recarga
  }
}

export function limpiarToken() {
  try {
    localStorage.removeItem(CLAVE_TOKEN)
  } catch {
    // nada que limpiar
  }
}

// FastAPI responde los errores como { detail: "texto" } o { detail: { message, fields } }.
function leerError(cuerpo, estado) {
  const detalle = cuerpo?.detail
  if (typeof detalle === 'string') return { mensaje: detalle, campos: {} }
  if (detalle && typeof detalle === 'object' && !Array.isArray(detalle)) {
    return { mensaje: detalle.message ?? 'Revisa los datos enviados.', campos: detalle.fields ?? {} }
  }
  return { mensaje: `La API respondió con el código ${estado}.`, campos: {} }
}

async function peticion(ruta, { metodo = 'GET', cuerpo, auth = true } = {}) {
  const cabeceras = {}
  if (cuerpo !== undefined) cabeceras['Content-Type'] = 'application/json'
  const token = obtenerToken()
  if (auth && token) cabeceras.Authorization = `Bearer ${token}`

  let respuesta
  try {
    respuesta = await fetch(urlApi(ruta), {
      method: metodo,
      headers: cabeceras,
      body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
    })
  } catch {
    throw new ApiError('No se pudo conectar con la API. Verifica que esté encendida (uvicorn api.app:app).')
  }

  if (respuesta.status === 204) return null
  const datos = await respuesta.json().catch(() => null)

  if (!respuesta.ok) {
    const { mensaje, campos } = leerError(datos, respuesta.status)
    if (respuesta.status === 401 && auth) {
      limpiarToken()
      window.dispatchEvent(new Event(EVENTO_SESION_EXPIRADA))
    }
    throw new ApiError(mensaje, respuesta.status, campos)
  }
  return datos
}

export const api = {
  get: (ruta, opciones) => peticion(ruta, opciones),
  post: (ruta, cuerpo, opciones) => peticion(ruta, { ...opciones, metodo: 'POST', cuerpo }),
  put: (ruta, cuerpo, opciones) => peticion(ruta, { ...opciones, metodo: 'PUT', cuerpo }),
  delete: (ruta, opciones) => peticion(ruta, { ...opciones, metodo: 'DELETE' }),
}
