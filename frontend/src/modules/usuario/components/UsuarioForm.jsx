import { useFormulario } from '../../core/hooks/useFormulario'
import Input from '../../core/design-system/Input'
import Select from '../../core/design-system/Select'
import Casilla from '../../core/design-system/Casilla'
import AccionesFormulario from '../../core/design-system/AccionesFormulario'
import { MENSAJE_CONTRASENA } from '../../core/utils/validaciones'
import { OPCIONES_ROL } from '../lib/constantes'
import { normalizarUsuario, validarUsuario } from '../utils/validarUsuario'

const VACIO = { nombre: '', correo: '', rol: '', activo: true }

export default function UsuarioForm({ item, onGuardar, onCancelar }) {
  const esNuevo = !item.id
  const { valores, errores, enviando, cambiar, enviar } = useFormulario(
    // La contraseña nunca viene de la API: siempre arranca vacía
    { ...VACIO, ...item, contrasena: '', confirmar: '' },
    (v) => validarUsuario(v, esNuevo),
    (datos) => onGuardar(normalizarUsuario(datos)),
  )

  return (
    <form className="formulario" onSubmit={enviar} noValidate>
      <div className="formulario__rejilla">
        <Input name="nombre" etiqueta="Nombre completo" ancho value={valores.nombre} onChange={cambiar} error={errores.nombre} />
        <Input name="correo" type="email" etiqueta="Correo" value={valores.correo} onChange={cambiar} error={errores.correo} />
        <Select name="rol" etiqueta="Rol" opciones={OPCIONES_ROL} value={valores.rol} onChange={cambiar} error={errores.rol} />
        <Input
          name="contrasena"
          type="password"
          etiqueta={esNuevo ? 'Contraseña' : 'Nueva contraseña'}
          autoComplete="new-password"
          ayuda={esNuevo ? MENSAJE_CONTRASENA : 'Déjala vacía para conservar la actual.'}
          value={valores.contrasena}
          onChange={cambiar}
          error={errores.contrasena}
        />
        <Input
          name="confirmar"
          type="password"
          etiqueta="Confirmar contraseña"
          autoComplete="new-password"
          value={valores.confirmar}
          onChange={cambiar}
          error={errores.confirmar}
        />
        <Casilla name="activo" etiqueta="Usuario activo" checked={valores.activo} onChange={cambiar} />
      </div>
      <AccionesFormulario onCancelar={onCancelar} enviando={enviando} error={errores.general} />
    </form>
  )
}
