import { moduloRegistros } from "../services/graficasRegistros";

/** Datos de la sección Registros (gráficas generadas por el backend). */
export function useRegistros() {
  return moduloRegistros;
}
