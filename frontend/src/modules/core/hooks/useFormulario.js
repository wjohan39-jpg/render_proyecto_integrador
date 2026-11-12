import { useState } from 'react'

// Maneja los valores de un formulario, sus errores y el envío.
// validar(valores) devuelve { campo: 'mensaje' }; los errores por campo de la API se muestran igual.
export function useFormulario(valoresIniciales, validar, alEnviar) {
  const [valores, setValores] = useState(valoresIniciales)
  const [errores, setErrores] = useState({})
  const [enviando, setEnviando] = useState(false)

  const cambiar = (e) => {
    const { name, value, type, checked } = e.target
    setValores((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value }))
    setErrores((prev) => ({ ...prev, [name]: undefined, general: undefined }))
  }

  const asignar = (cambios) => setValores((prev) => ({ ...prev, ...cambios }))

  const enviar = async (e) => {
    e.preventDefault()
    const nuevos = validar(valores)
    setErrores(nuevos)
    if (Object.values(nuevos).some(Boolean)) return
    setEnviando(true)
    try {
      await alEnviar(valores)
    } catch (error) {
      setErrores({ ...(error?.campos ?? {}), general: error?.message ?? 'No se pudo guardar.' })
    } finally {
      setEnviando(false)
    }
  }

  return { valores, errores, enviando, cambiar, asignar, enviar }
}
