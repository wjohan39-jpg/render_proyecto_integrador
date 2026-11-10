import { moduloEmpresas } from "../services/graficasEmpresas";

/** Datos de la sección Empresas (gráficas generadas por el backend). */
export function useEmpresas() {
  return moduloEmpresas;
}
