import type { ModuloReporte } from "../../core/lib/tipos";

export const moduloPrioridades: ModuloReporte = {
  id: "prioridades",
  nombre: "Prioridades",
  autor: "Dave",
  sobretitulo: "ANÁLISIS DE PRIORIDADES",
  titulo: "Prioridades",
  resumen: "Cómo se reparten los niveles de prioridad y cuánto tarda la respuesta en cada uno.",
  pie: "REPORTE DE PRIORIDADES",
  graficas: [
    {
      titulo: "Filas por nivel",
      descripcion: "Cantidad de filas registradas en cada nivel.",
      archivo: "prioridades_grafica_1.png",
      alt: "Gráfico de barras con la cantidad de filas por nivel.",
    },
    {
      titulo: "Días promedio de respuesta",
      descripcion: "Tiempo promedio de respuesta según la prioridad.",
      archivo: "prioridades_grafica_2.png",
      alt: "Gráfico de barras con los días promedio de respuesta por prioridad.",
    },
    {
      titulo: "Reparto de las prioridades",
      descripcion: "Porcentaje de filas que corresponde a cada prioridad.",
      archivo: "prioridades_grafica_3.png",
      alt: "Gráfico de torta con el reparto de las prioridades.",
    },
  ],
};
