/** 1 -> "01", 12 -> "12" */
export function conCeros(numero: number): string {
  return String(numero).padStart(2, "0");
}

// Sin separador de miles: muchos enteros son identificadores (NIT, teléfono).
const decimales = new Intl.NumberFormat("es-CO", { maximumFractionDigits: 2, useGrouping: false });

/** Texto de una celda de tabla: nulos, booleanos y números legibles. */
export function formatearCelda(valor: string | number | boolean | null): string {
  if (valor === null || valor === "") return "—";
  if (typeof valor === "boolean") return valor ? "Sí" : "No";
  if (typeof valor === "number") return Number.isInteger(valor) ? String(valor) : decimales.format(valor);
  return valor;
}
