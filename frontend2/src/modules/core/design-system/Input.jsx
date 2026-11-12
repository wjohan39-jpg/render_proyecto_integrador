import Campo, { atributosControl } from './Campo'

export default function Input({ id, name, etiqueta, error, ayuda, ancho, ...props }) {
  const idCampo = id ?? name
  return (
    <Campo id={idCampo} etiqueta={etiqueta} error={error} ayuda={ayuda} ancho={ancho}>
      <input name={name} {...atributosControl(idCampo, error)} {...props} />
    </Campo>
  )
}
