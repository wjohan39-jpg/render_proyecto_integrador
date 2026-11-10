import { useMemo, type ComponentType } from "react";
import BarraSuperior from "./modules/core/components/BarraSuperior";
import FondoAnimado from "./modules/core/components/FondoAnimado";
import NavegacionModulos from "./modules/core/components/NavegacionModulos";
import PiePagina from "./modules/core/components/PiePagina";
import EstadoCarga from "./modules/core/design-system/EstadoCarga";
import { useModuloActivo } from "./modules/core/hooks/useModuloActivo";
import { usePeticion } from "./modules/core/hooks/usePeticion";
import { API_URL, obtenerModulos } from "./modules/core/lib/api";
import PrioridadesReporte from "./modules/prioridades/components/PrioridadesReporte";
import RegistrosReporte from "./modules/registros/components/RegistrosReporte";
import EmpresasReporte from "./modules/empresas/components/EmpresasReporte";
import RetosReporte from "./modules/retos/components/RetosReporte";

/** Componente de React que pinta cada sección que entrega la API. */
const COMPONENTES: Record<string, ComponentType> = {
  prioridades: PrioridadesReporte,
  registros: RegistrosReporte,
  empresas: EmpresasReporte,
  retos: RetosReporte,
};

export default function App() {
  const { datos, cargando, error } = usePeticion(obtenerModulos, []);
  const modulos = useMemo(() => (datos ?? []).filter((m) => m.id in COMPONENTES), [datos]);
  const ids = useMemo(() => modulos.map((m) => m.id), [modulos]);
  const activo = useModuloActivo(ids);
  const seccion = modulos.find((m) => m.id === activo);
  const Componente = seccion ? COMPONENTES[seccion.id] : null;

  return (
    <>
      <FondoAnimado />
      <main className="pagina">
        <BarraSuperior />
        {modulos.length > 0 && <NavegacionModulos opciones={modulos} activo={activo ?? ""} />}
        <EstadoCarga
          cargando={cargando}
          error={error && `${error} (API: ${API_URL})`}
          textoCarga="Conectando con la API… (en Render el primer arranque puede tardar hasta un minuto)"
        />
        {Componente && seccion && <Componente key={seccion.id} />}
        {seccion && <PiePagina nombre={seccion.nombre} autor={seccion.autor} />}
      </main>
    </>
  );
}
