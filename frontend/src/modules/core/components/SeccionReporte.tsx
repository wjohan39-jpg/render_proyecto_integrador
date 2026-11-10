import type { ModuloReporte } from "../lib/tipos";
import TarjetaGrafica from "../design-system/TarjetaGrafica";
import { conCeros } from "../utils/formato";

interface Props {
  modulo: ModuloReporte;
}

export default function SeccionReporte({ modulo }: Props) {
  return (
    <>
      <section className="introduccion" id={`seccion-${modulo.id}`}>
        <p className="sobretitulo">{modulo.sobretitulo}</p>
        <div className="introduccion__fila">
          <h1>
            {modulo.titulo}
            <span>.</span>
          </h1>
          <p>{modulo.resumen}</p>
        </div>
        <div className="introduccion__pie">
          <span>{modulo.pie}</span>
          <span>{conCeros(modulo.graficas.length)} GRÁFICAS</span>
        </div>
      </section>

      <section className="galeria" aria-label={`Gráficas de ${modulo.nombre.toLowerCase()}`}>
        {modulo.graficas.map((grafica, indice) => (
          <TarjetaGrafica key={grafica.archivo} grafica={grafica} numero={indice + 1} />
        ))}
      </section>
    </>
  );
}
