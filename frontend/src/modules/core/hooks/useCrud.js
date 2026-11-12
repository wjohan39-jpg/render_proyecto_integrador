import { useCallback, useEffect, useRef, useState } from 'react'

// Conecta un servicio CRUD (crearCrudService) con el estado de React.
// Después de cada cambio vuelve a leer la lista para que la vista quede al día.
// activo = false evita la petición (por ejemplo, si el usuario no tiene permiso).
export function useCrud(servicio, { activo = true } = {}) {
  const [items, setItems] = useState([])
  const [cargando, setCargando] = useState(activo)
  const [error, setError] = useState(null)
  const montado = useRef(true)

  useEffect(() => {
    montado.current = true
    return () => {
      montado.current = false
    }
  }, [])

  const recargar = useCallback(async () => {
    if (!activo) return
    setCargando(true)
    setError(null)
    try {
      const datos = await servicio.obtenerTodos()
      if (montado.current) setItems(Array.isArray(datos) ? datos : [])
    } catch (fallo) {
      if (montado.current) setError(fallo)
    } finally {
      if (montado.current) setCargando(false)
    }
  }, [servicio, activo])

  useEffect(() => {
    recargar()
  }, [recargar])

  const crear = useCallback(
    async (datos) => {
      const nuevo = await servicio.crear(datos)
      await recargar()
      return nuevo
    },
    [servicio, recargar],
  )

  const actualizar = useCallback(
    async (id, datos) => {
      const actualizado = await servicio.actualizar(id, datos)
      await recargar()
      return actualizado
    },
    [servicio, recargar],
  )

  const eliminar = useCallback(
    async (id) => {
      await servicio.eliminar(id)
      await recargar()
    },
    [servicio, recargar],
  )

  return { items, cargando, error, recargar, crear, actualizar, eliminar }
}
