import { usePeticion } from "../../core/hooks/usePeticion";
import { obtenerRegistros, obtenerConsultaRegistros, obtenerDatosRegistros } from "../services/registrosApi";

/** Carga la sección Registros desde la API y expone cómo pedir sus consultas y datos. */
export function useRegistros() {
  const detalle = usePeticion(obtenerRegistros, []);
  return { detalle, cargarConsulta: obtenerConsultaRegistros, cargarDatos: obtenerDatosRegistros };
}
