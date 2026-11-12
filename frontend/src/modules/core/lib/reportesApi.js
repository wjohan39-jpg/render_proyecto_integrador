import { api } from './apiClient'

// Reportes de solo lectura que genera main.py (gráficas y consultas de cada sección).

/** GET /api/modulos/{id}: textos, gráficas y lista de consultas. */
export const obtenerReporte = (idModulo) => api.get(`/api/modulos/${idModulo}`, { auth: false })

/** GET /api/modulos/{id}/consultas/{numero} */
export const obtenerConsulta = (idModulo, numero) =>
  api.get(`/api/modulos/${idModulo}/consultas/${numero}`, { auth: false })
