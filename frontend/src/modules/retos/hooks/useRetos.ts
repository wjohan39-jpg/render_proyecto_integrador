import { usePeticion } from "../../core/hooks/usePeticion";
import { obtenerRetos, obtenerConsultaRetos, obtenerDatosRetos } from "../services/retosApi";

/** Carga la sección Retos desde la API y expone cómo pedir sus consultas y datos. */
export function useRetos() {
  const detalle = usePeticion(obtenerRetos, []);
  return { detalle, cargarConsulta: obtenerConsultaRetos, cargarDatos: obtenerDatosRetos };
}
