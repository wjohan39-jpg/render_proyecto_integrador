import { obtenerJson } from "../../core/lib/api";
import type { ModuloDetalle, PaginaDatos, ResultadoConsulta } from "../../core/lib/tipos";

const BASE = "/api/modulos/prioridades";

/** GET prioridades: textos, gráficas y lista de consultas. */
export function obtenerPrioridades(): Promise<ModuloDetalle> {
  return obtenerJson<ModuloDetalle>(BASE);
}

/** GET prioridades/consultas/{numero} */
export function obtenerConsultaPrioridades(numero: number): Promise<ResultadoConsulta> {
  return obtenerJson<ResultadoConsulta>(`${BASE}/consultas/${numero}`);
}

/** GET prioridades/datos?pagina=&tamano= */
export function obtenerDatosPrioridades(pagina: number, tamano: number): Promise<PaginaDatos> {
  return obtenerJson<PaginaDatos>(`${BASE}/datos?pagina=${pagina}&tamano=${tamano}`);
}
