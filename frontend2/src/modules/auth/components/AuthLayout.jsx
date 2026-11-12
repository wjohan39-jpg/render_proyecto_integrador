import FondoAnimado from '../../core/components/FondoAnimado'
import BarraSuperior from '../../core/components/BarraSuperior'
import PiePagina from '../../core/components/PiePagina'

const MODULOS = [
  { nombre: 'Empresas', autor: 'Wesly' },
  { nombre: 'Prioridades', autor: 'Dave' },
  { nombre: 'Retos', autor: 'Diego' },
  { nombre: 'Registros', autor: 'Jeferson' },
]

// Diseño compartido por Login y Registro: presentación a la izquierda y formulario en un panel de vidrio.
export default function AuthLayout({ titulo, subtitulo, children }) {
  return (
    <>
      <FondoAnimado />
      <div className="pagina">
        <BarraSuperior />
        <main className="acceso pagina__contenido">
          <section className="acceso__intro">
            <p className="sobretitulo">PLATAFORMA DE RETOS EMPRESARIALES</p>
            <h1>
              Proyecto integrador<span>.</span>
            </h1>
            <p>
              Gestiona las empresas aliadas, sus retos, las prioridades y el registro de cada participación. Consulta,
              crea, modifica y elimina la información conectada a la API del proyecto.
            </p>
            <ul className="acceso__modulos">
              {MODULOS.map(({ nombre, autor }) => (
                <li key={nombre}>
                  {nombre}
                  <span>{autor}</span>
                </li>
              ))}
            </ul>
          </section>

          <section className="panel acceso__panel" aria-labelledby="titulo-acceso">
            <h2 id="titulo-acceso">{titulo}</h2>
            <p>{subtitulo}</p>
            {children}
          </section>
        </main>
        <PiePagina />
      </div>
    </>
  )
}
