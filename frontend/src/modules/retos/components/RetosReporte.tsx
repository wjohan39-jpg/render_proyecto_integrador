import SeccionReporte from "../../core/components/SeccionReporte";
import { useRetos } from "../hooks/useRetos";

export default function RetosReporte() {
  const { detalle, cargarConsulta, cargarDatos } = useRetos();
  return <SeccionReporte detalle={detalle} cargarConsulta={cargarConsulta} cargarDatos={cargarDatos} />;
}
