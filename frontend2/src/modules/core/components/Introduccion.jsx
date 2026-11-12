// Encabezado grande de cada página: sobretítulo en mono, título con punto naranja,
// resumen a la derecha y una línea de pie (como la introducción del visor).
export default function Introduccion({ sobretitulo, titulo, resumen, pieIzquierda, pieDerecha }) {
  return (
    <section className="introduccion">
      <p className="sobretitulo">{sobretitulo}</p>
      <div className="introduccion__fila">
        <h1>
          {titulo}
          <span>.</span>
        </h1>
        {resumen && <p>{resumen}</p>}
      </div>
      {(pieIzquierda || pieDerecha) && (
        <div className="introduccion__pie">
          <span>{pieIzquierda}</span>
          <span>{pieDerecha}</span>
        </div>
      )}
    </section>
  )
}
