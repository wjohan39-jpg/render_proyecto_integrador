import SeccionReporte from "../../core/components/SeccionReporte";
import { useRegistros } from "../hooks/useRegistros";

export default function RegistrosReporte() {
  const { detalle, cargarConsulta, cargarDatos } = useRegistros();
  return <SeccionReporte detalle={detalle} cargarConsulta={cargarConsulta} cargarDatos={cargarDatos} />;
}
