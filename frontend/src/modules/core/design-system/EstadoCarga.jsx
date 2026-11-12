import { RefreshCw } from 'lucide-react'
import Boton from './Boton'

// Mensaje de "cargando" o de error mientras se consulta la API.
// pantalla = true lo centra en toda la ventana (validación de sesión).
export default function EstadoCarga({ cargando, error, textoCarga = 'Cargando datos de la API…', onReintentar, pantalla = false }) {
  if (error) {
    const texto = typeof error === 'string' ? error : error.message
    return (
      <div className="estado-carga estado-carga--error" role="alert">
        <span>No se pudo obtener la información: {texto}</span>
        {onReintentar && (
          <Boton icono={RefreshCw} onClick={onReintentar}>
            Reintentar
          </Boton>
        )}
      </div>
    )
  }
  if (cargando) {
    return (
      <p className={`estado-carga${pantalla ? ' estado-carga--pantalla' : ''}`} role="status">
        <span className="cargador" aria-hidden="true" />
        {textoCarga}
      </p>
    )
  }
  return null
}
