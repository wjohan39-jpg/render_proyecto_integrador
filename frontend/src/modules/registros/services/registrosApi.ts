import { obtenerJson } from "../../core/lib/api";
import type { ModuloDetalle, PaginaDatos, ResultadoConsulta } from "../../core/lib/tipos";

const BASE = "/api/modulos/registros";

/** GET registros: textos, gráficas y lista de consultas. */
export function obtenerRegistros(): Promise<ModuloDetalle> {
  return obtenerJson<ModuloDetalle>(BASE);
}

/** GET registros/consultas/{numero} */
export function obtenerConsultaRegistros(numero: number): Promise<ResultadoConsulta> {
  return obtenerJson<ResultadoConsulta>(`${BASE}/consultas/${numero}`);
}

/** GET registros/datos?pagina=&tamano= */
export function obtenerDatosRegistros(pagina: number, tamano: number): Promise<PaginaDatos> {
  return obtenerJson<PaginaDatos>(`${BASE}/datos?pagina=${pagina}&tamano=${tamano}`);
}
