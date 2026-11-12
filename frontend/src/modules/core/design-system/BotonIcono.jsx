// Botón pequeño solo con ícono (acciones de cada fila de la tabla).
export default function BotonIcono({ icono: Icono, etiqueta, peligro = false, ...props }) {
  return (
    <button
      type="button"
      className={`boton-icono${peligro ? ' boton-icono--peligro' : ''}`}
      aria-label={etiqueta}
      title={etiqueta}
      {...props}
    >
      <Icono aria-hidden="true" />
    </button>
  )
}
