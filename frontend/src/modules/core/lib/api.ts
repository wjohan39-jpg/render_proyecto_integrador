import type { ModuloResumen } from "./tipos";

/** URL base de la API. En Render se define con la variable VITE_API_URL. */
export const API_URL = (import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");

/** Convierte una ruta de la API (/api/...) en URL completa. */
export function urlApi(ruta: string): string {
  return `${API_URL}${ruta}`;
}

/** GET a la API; si responde con error, lanza el mensaje "detail" que envía FastAPI. */
export async function obtenerJson<T>(ruta: string): Promise<T> {
  const respuesta = await fetch(urlApi(ruta));
  if (!respuesta.ok) {
    let detalle: string | undefined;
    try {
      detalle = (await respuesta.json()).detail;
    } catch {
      detalle = undefined;
    }
    throw new Error(detalle ?? `La API respondió con el código ${respuesta.status}.`);
  }
  return respuesta.json() as Promise<T>;
}

export function obtenerModulos(): Promise<ModuloResumen[]> {
  return obtenerJson<ModuloResumen[]>("/api/modulos");
}
