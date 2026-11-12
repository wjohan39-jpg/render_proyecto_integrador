import { api } from './apiClient'

// Fábrica de servicios CRUD contra la API: /api/{recurso}
// Cada módulo crea el suyo: crearCrudService('empresas')
export function crearCrudService(recurso) {
  const ruta = `/api/${recurso}`
  const conId = (id) => `${ruta}/${encodeURIComponent(id)}`

  return {
    obtenerTodos: () => api.get(ruta),
    obtenerPorId: (id) => api.get(conId(id)),
    crear: (datos) => api.post(ruta, datos),
    actualizar: (id, datos) => api.put(conId(id), datos),
    eliminar: (id) => api.delete(conId(id)),
  }
}
