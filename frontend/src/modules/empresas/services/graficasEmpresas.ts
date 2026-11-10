import type { ModuloReporte } from "../../core/lib/tipos";

export const moduloEmpresas: ModuloReporte = {
  id: "empresas",
  nombre: "Empresas",
  autor: "Wesly",
  sobretitulo: "ANÁLISIS DE EMPRESAS",
  titulo: "Empresas",
  resumen: "Distribución de las empresas por sector y cuántas siguen activas en cada uno.",
  pie: "REPORTE DE EMPRESAS",
  graficas: [
    {
      titulo: "Empresas por sector",
      descripcion: "Cantidad de empresas registradas en cada sector.",
      archivo: "empresas_grafica_1.png",
      alt: "Gráfico de barras con la cantidad de empresas por sector.",
    },
    {
      titulo: "Activas vs inactivas",
      descripcion: "Proporción de empresas activas e inactivas.",
      archivo: "empresas_grafica_2.png",
      alt: "Gráfico de torta con empresas activas e inactivas.",
    },
    {
      titulo: "Activas e inactivas por sector",
      descripcion: "Estado de las empresas dentro de cada sector.",
      archivo: "empresas_grafica_3.png",
      alt: "Gráfico de barras apiladas con empresas activas e inactivas por sector.",
    },
  ],
};
