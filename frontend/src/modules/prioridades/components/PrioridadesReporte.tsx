import SeccionReporte from "../../core/components/SeccionReporte";
import { usePrioridades } from "../hooks/usePrioridades";

export default function PrioridadesReporte() {
  const modulo = usePrioridades();
  return <SeccionReporte modulo={modulo} />;
}
