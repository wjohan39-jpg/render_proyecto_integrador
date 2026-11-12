// Botón cuadrado del visor: borde gris, magenta al pasar el mouse.
// variante: 'normal' | 'primario' | 'peligro' | 'fantasma'
export default function Boton({
  variante = 'normal',
  activo = false,
  grande = false,
  bloque = false,
  icono: Icono,
  className = '',
  children,
  ...props
}) {
  const clases = [
    'boton',
    variante !== 'normal' && `boton--${variante}`,
    activo && 'boton--activo',
    grande && 'boton--grande',
    bloque && 'boton--bloque',
    className,
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <button type="button" className={clases} aria-pressed={activo || undefined} {...props}>
      {Icono && <Icono aria-hidden="true" />}
      {children}
    </button>
  )
}
