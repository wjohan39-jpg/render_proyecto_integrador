import SeccionReporte from "../../core/components/SeccionReporte";
import { useEmpresas } from "../hooks/useEmpresas";

export default function EmpresasReporte() {
  const { detalle, cargarConsulta, cargarDatos } = useEmpresas();
  return <SeccionReporte detalle={detalle} cargarConsulta={cargarConsulta} cargarDatos={cargarDatos} />;
}
