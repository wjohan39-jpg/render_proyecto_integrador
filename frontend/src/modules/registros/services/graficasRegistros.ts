import type { ModuloReporte } from "../../core/lib/tipos";

export const moduloRegistros: ModuloReporte = {
  id: "registros",
  nombre: "Registros",
  autor: "Jeferson",
  sobretitulo: "ANÁLISIS DE INSCRIPCIONES",
  titulo: "Registros",
  resumen: "Una vista clara de la actividad, el ritmo mensual y los retos más concurridos.",
  pie: "REPORTE DE PARTICIPACIONES",
  graficas: [
    {
      titulo: "Participaciones por estado",
      descripcion: "Distribución de registros según su estado.",
      archivo: "registros_grafica_1.png",
      alt: "Gráfico de barras con la cantidad de participaciones por estado.",
    },
    {
      titulo: "Participaciones por mes",
      descripcion: "Evolución mensual de las inscripciones.",
      archivo: "registros_grafica_2.png",
      alt: "Gráfico de líneas con participaciones agrupadas por mes.",
    },
    {
      titulo: "Retos con más participantes",
      descripcion: "Los diez retos con mayor cantidad de registros.",
      archivo: "registros_grafica_3.png",
      alt: "Gráfico de barras horizontales con los diez retos más populares.",
    },
  ],
};
