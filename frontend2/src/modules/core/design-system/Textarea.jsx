import Campo, { atributosControl } from './Campo'

export default function Textarea({ id, name, etiqueta, error, ayuda, ancho, rows = 3, ...props }) {
  const idCampo = id ?? name
  return (
    <Campo id={idCampo} etiqueta={etiqueta} error={error} ayuda={ayuda} ancho={ancho}>
      <textarea name={name} rows={rows} {...atributosControl(idCampo, error)} {...props} />
    </Campo>
  )
}
