import SeccionReporte from "../../core/components/SeccionReporte";
import { useEmpresas } from "../hooks/useEmpresas";

export default function EmpresasReporte() {
  const modulo = useEmpresas();
  return <SeccionReporte modulo={modulo} />;
}
