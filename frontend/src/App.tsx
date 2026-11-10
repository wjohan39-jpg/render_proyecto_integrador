import type { ComponentType } from "react";
import BarraSuperior from "./modules/core/components/BarraSuperior";
import NavegacionModulos from "./modules/core/components/NavegacionModulos";
import PiePagina from "./modules/core/components/PiePagina";
import { useModuloActivo } from "./modules/core/hooks/useModuloActivo";
import PrioridadesReporte from "./modules/prioridades/components/PrioridadesReporte";
import { moduloPrioridades } from "./modules/prioridades/services/graficasPrioridades";
import RegistrosReporte from "./modules/registros/components/RegistrosReporte";
import { moduloRegistros } from "./modules/registros/services/graficasRegistros";
import EmpresasReporte from "./modules/empresas/components/EmpresasReporte";
import { moduloEmpresas } from "./modules/empresas/services/graficasEmpresas";
import RetosReporte from "./modules/retos/components/RetosReporte";
import { moduloRetos } from "./modules/retos/services/graficasRetos";

interface Seccion {
  id: string;
  nombre: string;
  autor: string;
  Componente: ComponentType;
}

const SECCIONES: Seccion[] = [
  { id: moduloPrioridades.id, nombre: moduloPrioridades.nombre, autor: moduloPrioridades.autor, Componente: PrioridadesReporte },
  { id: moduloRegistros.id, nombre: moduloRegistros.nombre, autor: moduloRegistros.autor, Componente: RegistrosReporte },
  { id: moduloEmpresas.id, nombre: moduloEmpresas.nombre, autor: moduloEmpresas.autor, Componente: EmpresasReporte },
  { id: moduloRetos.id, nombre: moduloRetos.nombre, autor: moduloRetos.autor, Componente: RetosReporte },
];
const IDS = SECCIONES.map((seccion) => seccion.id);

export default function App() {
  const activo = useModuloActivo(IDS);
  const seccion = SECCIONES.find((s) => s.id === activo) ?? SECCIONES[0];
  const { Componente } = seccion;

  return (
    <main className="pagina">
      <BarraSuperior />
      <NavegacionModulos opciones={SECCIONES} activo={seccion.id} />
      <Componente />
      <PiePagina nombre={seccion.nombre} autor={seccion.autor} />
    </main>
  );
}
