/** Una grafica PNG generada por el backend en reportes/. */
export interface Grafica {
  titulo: string;
  descripcion: string;
  archivo: string;
  alt: string;
}

/** Datos de una seccion del panel (un desarrollador / una tabla). */
export interface ModuloReporte {
  id: string;
  nombre: string;
  autor: string;
  sobretitulo: string;
  titulo: string;
  resumen: string;
  pie: string;
  graficas: Grafica[];
}
