export default function BarraSuperior() {
  return (
    <header className="barra-superior">
      <a className="marca" href="#" aria-label="Proyecto Integrador Cesde, inicio del panel">
        <span className="marca__sello" aria-hidden="true">PI</span>
        <span className="marca__nombre">
          PROYECTO INTEGRADOR <strong>CESDE</strong>
        </span>
      </a>
      <span className="estado">
        <span className="estado__punto" />
        Conectado a la API
      </span>
    </header>
  );
}
