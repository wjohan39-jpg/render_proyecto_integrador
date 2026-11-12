// Etiqueta de estado en mono con un punto de color.
// color: 'gris' | 'verde' | 'amarillo' | 'rojo' | 'morado' | 'magenta' | 'naranja'
export default function Etiqueta({ color = 'gris', children }) {
  return <span className={`etiqueta etiqueta--${color}`}>{children}</span>
}
