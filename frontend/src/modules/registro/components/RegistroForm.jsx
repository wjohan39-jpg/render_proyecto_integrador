import { useFormulario } from '../../core/hooks/useFormulario'
import Input from '../../core/design-system/Input'
import Select from '../../core/design-system/Select'
import Textarea from '../../core/design-system/Textarea'
import AccionesFormulario from '../../core/design-system/AccionesFormulario'
import { aFechaHoraLocal, ahoraLocal } from '../../core/utils/formato'
import { opcionesRelacion } from '../../core/utils/opciones'
import { OPCIONES_ESTADO_REGISTRO } from '../lib/constantes'
import { normalizarRegistro, validarRegistro } from '../utils/validarRegistro'

// retos: lista para elegir el reto. usuarios: solo llega si quien edita es administrador;
// si no, el ID de usuario se escribe (por defecto, el de la sesión).
export default function RegistroForm({ item, retos, usuarios, idSesion, onGuardar, onCancelar }) {
  const esNuevo = !item.id
  const { valores, errores, enviando, cambiar, enviar } = useFormulario(
    {
      fecha_registro: esNuevo ? ahoraLocal() : aFechaHoraLocal(item.fecha_registro),
      estado: item.estado ?? 'INSCRITO',
      observacion: item.observacion ?? '',
      id_reto: item.id_reto ?? '',
      id_usuario: esNuevo ? idSesion : (item.id_usuario ?? ''),
    },
    validarRegistro,
    (datos) => onGuardar(normalizarRegistro(datos)),
  )

  return (
    <form className="formulario" onSubmit={enviar} noValidate>
      <div className="formulario__rejilla">
        <Input
          name="fecha_registro"
          type="datetime-local"
          etiqueta="Fecha y hora"
          value={valores.fecha_registro}
          onChange={cambiar}
          error={errores.fecha_registro}
        />
        <Select name="estado" etiqueta="Estado" opciones={OPCIONES_ESTADO_REGISTRO} value={valores.estado} onChange={cambiar} error={errores.estado} />
        <Select
          name="id_reto"
          etiqueta="Reto"
          placeholder="Sin reto"
          ancho
          opciones={opcionesRelacion(retos, (r) => r.nombre, valores.id_reto)}
          value={valores.id_reto}
          onChange={cambiar}
          error={errores.id_reto}
        />
        {usuarios ? (
          <Select
            name="id_usuario"
            etiqueta="Usuario"
            placeholder="Sin usuario"
            ancho
            opciones={opcionesRelacion(usuarios, (u) => `${u.nombre} · ${u.correo}`, valores.id_usuario)}
            value={valores.id_usuario}
            onChange={cambiar}
            error={errores.id_usuario}
          />
        ) : (
          <Input
            name="id_usuario"
            etiqueta="ID de usuario"
            ancho
            ayuda="Por defecto, tu propio usuario."
            value={valores.id_usuario}
            onChange={cambiar}
            error={errores.id_usuario}
          />
        )}
        <Textarea name="observacion" etiqueta="Observación" ancho value={valores.observacion} onChange={cambiar} error={errores.observacion} />
      </div>
      <AccionesFormulario onCancelar={onCancelar} enviando={enviando} error={errores.general} />
    </form>
  )
}
