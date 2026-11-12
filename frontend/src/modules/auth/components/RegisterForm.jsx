import { Link, useNavigate } from 'react-router-dom'
import { UserPlus } from 'lucide-react'
import { useFormulario } from '../../core/hooks/useFormulario'
import Input from '../../core/design-system/Input'
import Select from '../../core/design-system/Select'
import Boton from '../../core/design-system/Boton'
import Aviso from '../../core/design-system/Aviso'
import { INICIO } from '../../core/lib/menu'
import { MENSAJE_CONTRASENA } from '../../core/utils/validaciones'
import { useAuth } from '../hooks/useAuth'
import { validarRegistro } from '../utils/validarAuth'
import { opcionesRol, ROLES_REGISTRO } from '../lib/constantes'

const OPCIONES_ROL = opcionesRol(ROLES_REGISTRO)

export default function RegisterForm() {
  const { registrar } = useAuth()
  const navigate = useNavigate()

  const { valores, errores, enviando, cambiar, enviar } = useFormulario(
    { nombre: '', correo: '', rol: '', contrasena: '', confirmar: '' },
    validarRegistro,
    async (datos) => {
      await registrar(datos)
      navigate(INICIO, { replace: true })
    },
  )

  return (
    <form className="formulario" onSubmit={enviar} noValidate>
      {errores.general && <Aviso>{errores.general}</Aviso>}

      <Input name="nombre" etiqueta="Nombre completo" autoComplete="name" value={valores.nombre} onChange={cambiar} error={errores.nombre} />
      <Input name="correo" type="email" etiqueta="Correo electrónico" autoComplete="email" value={valores.correo} onChange={cambiar} error={errores.correo} />
      <Select name="rol" etiqueta="Rol" opciones={OPCIONES_ROL} value={valores.rol} onChange={cambiar} error={errores.rol} />
      <div className="formulario__rejilla">
        <Input
          name="contrasena"
          type="password"
          etiqueta="Contraseña"
          autoComplete="new-password"
          value={valores.contrasena}
          onChange={cambiar}
          error={errores.contrasena}
          ayuda={MENSAJE_CONTRASENA}
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
      </div>

      <Boton type="submit" variante="primario" grande bloque icono={UserPlus} disabled={enviando}>
        {enviando ? 'Creando cuenta…' : 'Crear cuenta'}
      </Boton>

      <p className="acceso__pie">
        ¿Ya tienes cuenta?{' '}
        <Link to="/login" className="enlace">
          Inicia sesión
        </Link>
      </p>
    </form>
  )
}
