import type { ModuloReporte } from "../../core/lib/tipos";

export const moduloRetos: ModuloReporte = {
  id: "retos",
  nombre: "Retos",
  autor: "Diego",
  sobretitulo: "ANÁLISIS DE RETOS",
  titulo: "Retos",
  resumen: "Estado de los retos, cuántos arrancan cada mes y cuánto suelen durar.",
  pie: "REPORTE DE RETOS",
  graficas: [
    {
      titulo: "Retos por estado",
      descripcion: "Cantidad de retos en cada estado.",
      archivo: "retos_grafica_1.png",
      alt: "Gráfico de barras con la cantidad de retos por estado.",
    },
    {
      titulo: "Retos que empiezan cada mes",
      descripcion: "Evolución mensual del inicio de retos.",
      archivo: "retos_grafica_2.png",
      alt: "Gráfico de líneas con los retos que empiezan cada mes.",
    },
    {
      titulo: "Duración de los retos",
      descripcion: "Cómo se reparte la duración de los retos.",
      archivo: "retos_grafica_3.png",
      alt: "Histograma con la distribución de la duración de los retos.",
    },
  ],
};
