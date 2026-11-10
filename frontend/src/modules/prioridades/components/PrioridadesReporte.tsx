import SeccionReporte from "../../core/components/SeccionReporte";
import { usePrioridades } from "../hooks/usePrioridades";

export default function PrioridadesReporte() {
  const { detalle, cargarConsulta, cargarDatos } = usePrioridades();
  return <SeccionReporte detalle={detalle} cargarConsulta={cargarConsulta} cargarDatos={cargarDatos} />;
}
