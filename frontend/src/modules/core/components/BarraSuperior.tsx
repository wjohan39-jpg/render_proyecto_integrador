export default function BarraSuperior() {
  return (
    <header className="barra-superior">
      <a className="marca" href="#" aria-label="Inicio del panel">
        <span className="marca__sello">PI</span>
        <span>PROYECTO INTEGRADOR</span>
      </a>
      <span className="estado">
        <span className="estado__punto" />
        Reportes locales
      </span>
    </header>
  );
}
