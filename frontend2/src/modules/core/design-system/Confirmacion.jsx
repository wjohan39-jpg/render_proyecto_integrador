import { useState } from 'react'
import Modal from './Modal'
import Boton from './Boton'

// Pide confirmación antes de una acción que no se puede deshacer (eliminar).
export default function Confirmacion({ abierto, titulo = '¿Eliminar este elemento?', mensaje, textoConfirmar = 'Eliminar', onConfirmar, onCancelar }) {
  const [confirmando, setConfirmando] = useState(false)

  const confirmar = async () => {
    if (confirmando) return
    setConfirmando(true)
    try {
      await onConfirmar()
    } finally {
      setConfirmando(false)
    }
  }

  return (
    <Modal abierto={abierto} titulo={titulo} onCerrar={onCancelar} angosta>
      <p className="modal__texto">{mensaje}</p>
      <div className="formulario__acciones">
        <Boton onClick={onCancelar} disabled={confirmando}>
          Cancelar
        </Boton>
        <Boton variante="peligro" onClick={confirmar} disabled={confirmando}>
          {confirmando ? 'Eliminando…' : textoConfirmar}
        </Boton>
      </div>
    </Modal>
  )
}
