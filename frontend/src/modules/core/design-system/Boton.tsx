import type { ButtonHTMLAttributes } from "react";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  activo?: boolean;
}

export default function Boton({ activo = false, className = "", ...resto }: Props) {
  return (
    <button
      type="button"
      className={`boton${activo ? " boton--activo" : ""} ${className}`.trim()}
      aria-pressed={activo || undefined}
      {...resto}
    />
  );
}
