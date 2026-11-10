import Pestana from "../design-system/Pestana";

interface Opcion {
  id: string;
  nombre: string;
  autor: string;
}

interface Props {
  opciones: readonly Opcion[];
  activo: string;
}

export default function NavegacionModulos({ opciones, activo }: Props) {
  return (
    <nav className="navegacion" aria-label="Secciones del proyecto">
      {opciones.map((opcion) => (
        <Pestana
          key={opcion.id}
          href={`#${opcion.id}`}
          activa={opcion.id === activo}
          titulo={opcion.nombre}
          detalle={opcion.autor}
        />
      ))}
    </nav>
  );
}
