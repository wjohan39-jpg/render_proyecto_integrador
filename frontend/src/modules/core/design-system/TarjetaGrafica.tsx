import type { Grafica } from "../lib/tipos";
import { urlApi } from "../lib/api";
import { conCeros } from "../utils/formato";

interface Props {
  grafica: Grafica;
}

export default function TarjetaGrafica({ grafica }: Props) {
  const ruta = urlApi(grafica.url);
  return (
    <article className="grafica">
      <header className="grafica__encabezado">
        <span className="grafica__numero">{conCeros(grafica.numero)}</span>
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
        <img src={ruta} alt={grafica.alt} loading="lazy" />
      </a>
    </article>
  );
}
