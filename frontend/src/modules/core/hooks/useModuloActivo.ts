import { useEffect, useState } from "react";

/** Devuelve el id del modulo indicado en la URL (#empresas); si no hay, el primero. */
export function useModuloActivo(ids: readonly string[]): string {
  const leer = () => {
    const hash = window.location.hash.slice(1);
    return ids.includes(hash) ? hash : ids[0];
  };
  const [activo, setActivo] = useState(leer);

  useEffect(() => {
    const alCambiar = () => setActivo(leer());
    window.addEventListener("hashchange", alCambiar);
    return () => window.removeEventListener("hashchange", alCambiar);
  }, [ids]);

  return activo;
}
