import Campo, { atributosControl } from './Campo'

// opciones: [{ valor, texto }]
export default function Select({
  id,
  name,
  etiqueta,
  error,
  ayuda,
  ancho,
  opciones = [],
  placeholder = 'Selecciona una opción',
  ...props
}) {
  const idCampo = id ?? name
  return (
    <Campo id={idCampo} etiqueta={etiqueta} error={error} ayuda={ayuda} ancho={ancho}>
      <select name={name} {...atributosControl(idCampo, error)} {...props}>
        {placeholder !== null && <option value="">{placeholder}</option>}
        {opciones.map((op) => (
          <option key={op.valor} value={op.valor}>
            {op.texto}
          </option>
        ))}
      </select>
    </Campo>
  )
}
