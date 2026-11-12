import Etiqueta from '../../core/design-system/Etiqueta'
import { formatearFecha } from '../../core/utils/formato'
import { COLOR_ROL } from '../lib/constantes'

// Columnas de la tabla de usuarios. idSesion marca la fila del usuario conectado.
export function crearColumnasUsuario(idSesion) {
  return [
    { clave: 'nombre', titulo: 'Nombre', render: (u) => (u.id === idSesion ? `${u.nombre} (tú)` : u.nombre) },
    { clave: 'correo', titulo: 'Correo' },
    { clave: 'rol', titulo: 'Rol', render: (u) => <Etiqueta color={COLOR_ROL[u.rol]}>{u.rol}</Etiqueta> },
    { clave: 'activo', titulo: 'Estado', render: (u) => <Etiqueta color={u.activo ? 'verde' : 'gris'}>{u.activo ? 'Activo' : 'Inactivo'}</Etiqueta> },
    { clave: 'fecha_registro', titulo: 'Registrado', render: (u) => formatearFecha(u.fecha_registro) },
  ]
}
