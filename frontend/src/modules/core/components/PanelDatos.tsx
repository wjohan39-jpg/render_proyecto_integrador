import { useState } from "react";
import type { CargarDatos } from "../lib/tipos";
import { usePeticion } from "../hooks/usePeticion";
import Boton from "../design-system/Boton";
import EstadoCarga from "../design-system/EstadoCarga";
import TablaDatos from "../design-system/TablaDatos";

const TAMANO_PAGINA = 10;

interface Props {
  nombre: string;
  cargarDatos: CargarDatos;
}

export default function PanelDatos({ nombre, cargarDatos }: Props) {
  const [pagina, setPagina] = useState(1);
  const { datos, cargando, error } = usePeticion(
    () => cargarDatos(pagina, TAMANO_PAGINA),
    [pagina, cargarDatos],
  );
  const totalPaginas = datos ? Math.max(1, Math.ceil(datos.total / TAMANO_PAGINA)) : 1;

  return (
    <section className="panel" aria-labelledby="titulo-datos">
      <header className="panel__encabezado">
        <h2 id="titulo-datos">Datos limpios</h2>
        <div className="panel__acciones">
          <Boton onClick={() => setPagina((p) => p - 1)} disabled={pagina <= 1 || cargando}>
            Anterior
          </Boton>
          <span className="panel__pagina">
            Página {pagina} de {totalPaginas}
          </span>
          <Boton onClick={() => setPagina((p) => p + 1)} disabled={pagina >= totalPaginas || cargando}>
            Siguiente
          </Boton>
        </div>
      </header>

      <EstadoCarga cargando={cargando && !datos} error={error} />
      {datos && (
        <>
          <TablaDatos columnas={datos.columnas} filas={datos.filas} titulo={`Datos de ${nombre}`} />
          <p className="panel__nota">{datos.total} filas en total.</p>
        </>
      )}
    </section>
  );
}
