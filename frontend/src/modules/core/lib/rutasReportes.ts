// Vite sirve la carpeta ../reportes como raiz publica (ver vite.config.js).
export function rutaReporte(archivo: string): string {
  return `${import.meta.env.BASE_URL}${archivo}`;
}
