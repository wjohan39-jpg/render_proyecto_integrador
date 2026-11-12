// Envoltura común de los campos: etiqueta + control + ayuda o error.
export default function Campo({ id, etiqueta, error, ayuda, ancho = false, children }) {
  return (
    <div className={`campo${ancho ? ' campo--ancho' : ''}`}>
      {etiqueta && (
        <label htmlFor={id} className="campo__etiqueta">
          {etiqueta}
        </label>
      )}
      {children}
      {error ? (
        <p className="campo__error" id={`${id}-error`}>
          {error}
        </p>
      ) : (
        ayuda && <p className="campo__ayuda">{ayuda}</p>
      )}
    </div>
  )
}

// Atributos de accesibilidad que comparten Input, Select y Textarea.
export const atributosControl = (id, error) => ({
  id,
  className: 'control',
  'aria-invalid': Boolean(error),
  'aria-describedby': error ? `${id}-error` : undefined,
})
