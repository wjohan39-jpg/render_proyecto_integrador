import type { CargarConsulta, CargarDatos, ModuloDetalle } from "../lib/tipos";
import type { EstadoPeticion } from "../hooks/usePeticion";
import TarjetaGrafica from "../design-system/TarjetaGrafica";
import EstadoCarga from "../design-system/EstadoCarga";
import PanelConsultas from "./PanelConsultas";
import PanelDatos from "./PanelDatos";
import { conCeros } from "../utils/formato";

interface Props {
  detalle: EstadoPeticion<ModuloDetalle>;
  cargarConsulta: CargarConsulta;
  cargarDatos: CargarDatos;
}

export default function SeccionReporte({ detalle, cargarConsulta, cargarDatos }: Props) {
  const modulo = detalle.datos;
  if (!modulo) {
    return <EstadoCarga cargando={detalle.cargando} error={detalle.error} />;
  }

  return (
    <>
      <section className="introduccion">
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
          <span>
            {modulo.totalRegistros} REGISTROS · {conCeros(modulo.graficas.length)} GRÁFICAS
          </span>
        </div>
      </section>

      <section className="galeria" aria-label={`Gráficas de ${modulo.nombre.toLowerCase()}`}>
        {modulo.graficas.map((grafica) => (
          <TarjetaGrafica key={grafica.numero} grafica={grafica} />
        ))}
      </section>

      <PanelConsultas key={`c-${modulo.id}`} consultas={modulo.consultas} cargarConsulta={cargarConsulta} />
      <PanelDatos key={`d-${modulo.id}`} nombre={modulo.nombre} cargarDatos={cargarDatos} />
    </>
  );
}
