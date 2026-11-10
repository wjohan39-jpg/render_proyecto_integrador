/** 1 -> "01", 12 -> "12" */
export function conCeros(numero: number): string {
  return String(numero).padStart(2, "0");
}
