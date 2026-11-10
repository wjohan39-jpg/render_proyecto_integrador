import { useEffect, useState } from "react";

/** Devuelve el id del módulo indicado en la URL (#empresas); si no es válido, el primero. */
export function useModuloActivo(ids: readonly string[]): string | undefined {
  const [hash, setHash] = useState(() => window.location.hash.slice(1));

  useEffect(() => {
    const alCambiar = () => setHash(window.location.hash.slice(1));
    window.addEventListener("hashchange", alCambiar);
    return () => window.removeEventListener("hashchange", alCambiar);
  }, []);

  return ids.includes(hash) ? hash : ids[0];
}
