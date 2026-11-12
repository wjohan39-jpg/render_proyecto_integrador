import Etiqueta from '../../core/design-system/Etiqueta'

// Columnas de la tabla de empresas.
export const COLUMNAS_EMPRESA = [
  { clave: 'nombre', titulo: 'Nombre' },
  { clave: 'nit', titulo: 'NIT', clase: 'celda-mono' },
  { clave: 'sector', titulo: 'Sector' },
  { clave: 'contacto', titulo: 'Contacto' },
  { clave: 'correo', titulo: 'Correo' },
  { clave: 'telefono', titulo: 'Teléfono', clase: 'celda-mono' },
  {
    clave: 'activa',
    titulo: 'Estado',
    render: (e) => <Etiqueta color={e.activa ? 'verde' : 'gris'}>{e.activa ? 'Activa' : 'Inactiva'}</Etiqueta>,
  },
]
