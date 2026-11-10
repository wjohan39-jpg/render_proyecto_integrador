import type { Grafica } from "../lib/tipos";
import { rutaReporte } from "../lib/rutasReportes";
import { conCeros } from "../utils/formato";

interface Props {
  grafica: Grafica;
  numero: number;
}

export default function TarjetaGrafica({ grafica, numero }: Props) {
  const ruta = rutaReporte(grafica.archivo);
  return (
    <article className="grafica">
      <header className="grafica__encabezado">
        <span className="grafica__numero">{conCeros(numero)}</span>
        <div>
          <h2>{grafica.titulo}</h2>
          <p>{grafica.descripcion}</p>
        </div>
      </header>
      <a
        className="grafica__imagen-enlace"
        href={ruta}
        target="_blank"
        rel="noreferrer"
        aria-label={`Abrir gráfica: ${grafica.titulo}`}
      >
        <img src={ruta} alt={grafica.alt} />
      </a>
    </article>
  );
}
