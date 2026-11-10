interface Props {
  cargando: boolean;
  error: string | null;
  textoCarga?: string;
}

/** Mensaje de "cargando" o de error mientras se consulta la API. */
export default function EstadoCarga({ cargando, error, textoCarga = "Cargando datos de la API…" }: Props) {
  if (error) {
    return (
      <p className="estado-carga estado-carga--error" role="alert">
        No se pudo obtener la información: {error}
      </p>
    );
  }
  if (cargando) {
    return (
      <p className="estado-carga" role="status">
        {textoCarga}
      </p>
    );
  }
  return null;
}
