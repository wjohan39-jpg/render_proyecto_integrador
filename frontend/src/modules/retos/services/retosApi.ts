import { obtenerJson } from "../../core/lib/api";
import type { ModuloDetalle, PaginaDatos, ResultadoConsulta } from "../../core/lib/tipos";

const BASE = "/api/modulos/retos";

/** GET retos: textos, gráficas y lista de consultas. */
export function obtenerRetos(): Promise<ModuloDetalle> {
  return obtenerJson<ModuloDetalle>(BASE);
}

/** GET retos/consultas/{numero} */
export function obtenerConsultaRetos(numero: number): Promise<ResultadoConsulta> {
  return obtenerJson<ResultadoConsulta>(`${BASE}/consultas/${numero}`);
}

/** GET retos/datos?pagina=&tamano= */
export function obtenerDatosRetos(pagina: number, tamano: number): Promise<PaginaDatos> {
  return obtenerJson<PaginaDatos>(`${BASE}/datos?pagina=${pagina}&tamano=${tamano}`);
}
