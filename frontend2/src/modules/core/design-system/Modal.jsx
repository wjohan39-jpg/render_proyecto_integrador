import { useEffect, useId, useRef } from 'react'
import { X } from 'lucide-react'
import BotonIcono from './BotonIcono'

// Ventana modal: se cierra con Escape, con la × o haciendo clic fuera.
export default function Modal({ abierto, titulo, onCerrar, angosta = false, children }) {
  const idTitulo = useId()
  const cajaRef = useRef(null)
  const cerrarRef = useRef(onCerrar)
  cerrarRef.current = onCerrar

  // Solo al abrir: Escape cierra, el foco va al primer campo y al cerrar vuelve a donde estaba.
  useEffect(() => {
    if (!abierto) return
    const anterior = document.activeElement
    const alPresionar = (e) => e.key === 'Escape' && cerrarRef.current()
    window.addEventListener('keydown', alPresionar)
    cajaRef.current?.querySelector('input, select, textarea, button:not([aria-label="Cerrar"])')?.focus()
    return () => {
      window.removeEventListener('keydown', alPresionar)
      anterior?.focus?.()
    }
  }, [abierto])

  if (!abierto) return null

  return (
    <div className="modal">
      <div className="modal__fondo" onClick={onCerrar} aria-hidden="true" />
      <div
        ref={cajaRef}
        className={`modal__caja${angosta ? ' modal__caja--angosta' : ''}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby={idTitulo}
      >
        <header className="modal__encabezado">
          <h2 id={idTitulo}>{titulo}</h2>
          <BotonIcono icono={X} etiqueta="Cerrar" onClick={onCerrar} />
        </header>
        <div className="modal__cuerpo">{children}</div>
      </div>
    </div>
  )
}
