import { useEffect, useState, type DependencyList } from "react";

export interface EstadoPeticion<T> {
  datos: T | null;
  cargando: boolean;
  error: string | null;
}

/** Ejecuta una petición a la API cada vez que cambian las dependencias. */
export function usePeticion<T>(cargar: () => Promise<T>, dependencias: DependencyList): EstadoPeticion<T> {
  const [estado, setEstado] = useState<EstadoPeticion<T>>({ datos: null, cargando: true, error: null });

  useEffect(() => {
    let vigente = true;
    setEstado((anterior) => ({ ...anterior, cargando: true, error: null }));
    cargar()
      .then((datos) => vigente && setEstado({ datos, cargando: false, error: null }))
      .catch((error: unknown) => {
        if (!vigente) return;
        const mensaje = error instanceof Error ? error.message : "Error desconocido.";
        setEstado({ datos: null, cargando: false, error: mensaje });
      });
    return () => {
      vigente = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencias);

  return estado;
}
