import { useCallback, useEffect, useState } from 'react'

// Ejecuta una petición a la API cada vez que cambian las dependencias.
// Devuelve { datos, cargando, error, recargar }.
export function usePeticion(cargar, dependencias) {
  const [estado, setEstado] = useState({ datos: null, cargando: true, error: null })
  const [version, setVersion] = useState(0)

  useEffect(() => {
    let vigente = true
    setEstado((anterior) => ({ ...anterior, cargando: true, error: null }))
    cargar()
      .then((datos) => vigente && setEstado({ datos, cargando: false, error: null }))
      .catch((error) => vigente && setEstado({ datos: null, cargando: false, error }))
    return () => {
      vigente = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...dependencias, version])

  const recargar = useCallback(() => setVersion((v) => v + 1), [])
  return { ...estado, recargar }
}
