import Boton from './Boton'
import Aviso from './Aviso'

// Pie de los formularios: error general + botones Cancelar / Guardar.
export default function AccionesFormulario({ onCancelar, enviando, error, textoGuardar = 'Guardar' }) {
  return (
    <>
      {error && <Aviso>{error}</Aviso>}
      <div className="formulario__acciones">
        <Boton onClick={onCancelar} disabled={enviando}>
          Cancelar
        </Boton>
        <Boton type="submit" variante="primario" disabled={enviando}>
          {enviando ? 'Guardando…' : textoGuardar}
        </Boton>
      </div>
    </>
  )
}
