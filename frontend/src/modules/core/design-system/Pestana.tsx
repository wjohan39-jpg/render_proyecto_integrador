interface Props {
  href: string;
  activa: boolean;
  titulo: string;
  detalle: string;
}

export default function Pestana({ href, activa, titulo, detalle }: Props) {
  return (
    <a
      className={`pestana${activa ? " pestana--activa" : ""}`}
      href={href}
      aria-current={activa ? "page" : undefined}
    >
      <span className="pestana__titulo">{titulo}</span>
      <span className="pestana__detalle">{detalle}</span>
    </a>
  );
}
