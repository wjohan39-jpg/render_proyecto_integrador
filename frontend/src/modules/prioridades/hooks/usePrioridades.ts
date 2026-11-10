import { usePeticion } from "../../core/hooks/usePeticion";
import { obtenerPrioridades, obtenerConsultaPrioridades, obtenerDatosPrioridades } from "../services/prioridadesApi";

/** Carga la sección Prioridades desde la API y expone cómo pedir sus consultas y datos. */
export function usePrioridades() {
  const detalle = usePeticion(obtenerPrioridades, []);
  return { detalle, cargarConsulta: obtenerConsultaPrioridades, cargarDatos: obtenerDatosPrioridades };
}
