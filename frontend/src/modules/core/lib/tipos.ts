/** Tipos de las respuestas de la API (api/app.py). */

export interface ModuloResumen {
  id: string;
  nombre: string;
  autor: string;
}

export interface Grafica {
  numero: number;
  titulo: string;
  descripcion: string;
  alt: string;
  url: string;
}

export interface ConsultaInfo {
  numero: number;
  titulo: string;
  url: string;
}

export interface ModuloDetalle extends ModuloResumen {
  sobretitulo: string;
  titulo: string;
  resumen: string;
  pie: string;
  totalRegistros: number;
  graficas: Grafica[];
  consultas: ConsultaInfo[];
}

export type Fila = Record<string, string | number | boolean | null>;

export interface ResultadoConsulta {
  numero: number;
  titulo: string;
  columnas: string[];
  total: number;
  filas: Fila[];
}

export interface PaginaDatos {
  pagina: number;
  tamano: number;
  total: number;
  columnas: string[];
  filas: Fila[];
}

/** Funciones que cada módulo entrega para cargar sus consultas y sus datos. */
export type CargarConsulta = (numero: number) => Promise<ResultadoConsulta>;
export type CargarDatos = (pagina: number, tamano: number) => Promise<PaginaDatos>;
