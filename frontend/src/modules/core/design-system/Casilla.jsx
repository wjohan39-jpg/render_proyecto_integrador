// Casilla de verificación con su texto (por ejemplo "Empresa activa").
export default function Casilla({ etiqueta, ...props }) {
  return (
    <label className="casilla">
      <input type="checkbox" {...props} />
      {etiqueta}
    </label>
  )
}
