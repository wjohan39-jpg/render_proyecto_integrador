import { createContext, useEffect, useState } from 'react'
import * as authService from '../services/authService'
import { EVENTO_SESION_EXPIRADA } from '../../core/lib/apiClient'

export const AuthContext = createContext(null)

// Guarda el usuario con sesión y lo comparte con toda la aplicación.
// Al cargar la página valida el token contra /api/auth/me.
export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(() => authService.obtenerSesion())
  const [cargandoSesion, setCargandoSesion] = useState(true)

  useEffect(() => {
    let activo = true
    authService
      .restaurarSesion()
      .then((sesion) => activo && setUsuario(sesion))
      .finally(() => activo && setCargandoSesion(false))
    return () => {
      activo = false
    }
  }, [])

  // Si la API responde 401 en cualquier petición, se vuelve al login.
  useEffect(() => {
    const alExpirar = () => {
      authService.olvidarSesion()
      setUsuario(null)
    }
    window.addEventListener(EVENTO_SESION_EXPIRADA, alExpirar)
    return () => window.removeEventListener(EVENTO_SESION_EXPIRADA, alExpirar)
  }, [])

  const iniciarSesion = async (correo, contrasena) => {
    const sesion = await authService.iniciarSesion(correo, contrasena)
    setUsuario(sesion)
    return sesion
  }

  const registrar = async (datos) => {
    const sesion = await authService.registrar(datos)
    setUsuario(sesion)
    return sesion
  }

  const cerrarSesion = async () => {
    await authService.cerrarSesion()
    setUsuario(null)
  }

  const valor = {
    usuario,
    esAdministrador: usuario?.rol === 'administrador',
    cargandoSesion,
    iniciarSesion,
    registrar,
    cerrarSesion,
  }

  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>
}
