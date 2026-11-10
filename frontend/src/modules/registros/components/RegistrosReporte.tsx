import SeccionReporte from "../../core/components/SeccionReporte";
import { useRegistros } from "../hooks/useRegistros";

export default function RegistrosReporte() {
  const modulo = useRegistros();
  return <SeccionReporte modulo={modulo} />;
}
