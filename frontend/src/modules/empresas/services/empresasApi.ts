import { obtenerJson } from "../../core/lib/api";
import type { ModuloDetalle, PaginaDatos, ResultadoConsulta } from "../../core/lib/tipos";

const BASE = "/api/modulos/empresas";

/** GET empresas: textos, gráficas y lista de consultas. */
export function obtenerEmpresas(): Promise<ModuloDetalle> {
  return obtenerJson<ModuloDetalle>(BASE);
}

/** GET empresas/consultas/{numero} */
export function obtenerConsultaEmpresas(numero: number): Promise<ResultadoConsulta> {
  return obtenerJson<ResultadoConsulta>(`${BASE}/consultas/${numero}`);
}

/** GET empresas/datos?pagina=&tamano= */
export function obtenerDatosEmpresas(pagina: number, tamano: number): Promise<PaginaDatos> {
  return obtenerJson<PaginaDatos>(`${BASE}/datos?pagina=${pagina}&tamano=${tamano}`);
}
