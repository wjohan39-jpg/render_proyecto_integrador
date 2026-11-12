import { CircleAlert, CircleCheck } from 'lucide-react'

// Mensaje de éxito o de error. Con onCerrar muestra la ×.
export default function Aviso({ tipo = 'error', children, onCerrar }) {
  const esError = tipo === 'error'
  const Icono = esError ? CircleAlert : CircleCheck
  return (
    <div className={`aviso aviso--${esError ? 'error' : 'exito'}`} role={esError ? 'alert' : 'status'}>
      <Icono aria-hidden="true" />
      <div className="aviso__texto">{children}</div>
      {onCerrar && (
        <button type="button" className="aviso__cerrar" onClick={onCerrar} aria-label="Cerrar aviso">
          ×
        </button>
      )}
    </div>
  )
}
