import SeccionReporte from "../../core/components/SeccionReporte";
import { useRetos } from "../hooks/useRetos";

export default function RetosReporte() {
  const modulo = useRetos();
  return <SeccionReporte modulo={modulo} />;
}
