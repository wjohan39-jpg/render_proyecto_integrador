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
      <span>Imágenes generadas por el reporte local</span>
    </footer>
  );
}
