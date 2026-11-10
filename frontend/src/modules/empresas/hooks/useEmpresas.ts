import { usePeticion } from "../../core/hooks/usePeticion";
import { obtenerEmpresas, obtenerConsultaEmpresas, obtenerDatosEmpresas } from "../services/empresasApi";

/** Carga la sección Empresas desde la API y expone cómo pedir sus consultas y datos. */
export function useEmpresas() {
  const detalle = usePeticion(obtenerEmpresas, []);
  return { detalle, cargarConsulta: obtenerConsultaEmpresas, cargarDatos: obtenerDatosEmpresas };
}
