interface Props {
  nombre: string;
  autor: string;
}

export default function PiePagina({ nombre, autor }: Props) {
  return (
    <footer className="pie-pagina">
      <span>
        Proyecto integrador · {nombre} · {autor}
      </span>
      <span>Datos servidos por la API del proyecto</span>
    </footer>
  );
}
