import { useFormulario } from '../../core/hooks/useFormulario'
import Input from '../../core/design-system/Input'
import Select from '../../core/design-system/Select'
import Casilla from '../../core/design-system/Casilla'
import AccionesFormulario from '../../core/design-system/AccionesFormulario'
import { OPCIONES_SECTOR } from '../lib/constantes'
import { normalizarEmpresa, validarEmpresa } from '../utils/validarEmpresa'

const VACIA = { nombre: '', nit: '', sector: '', contacto: '', correo: '', telefono: '', activa: true }

export default function EmpresaForm({ item, onGuardar, onCancelar }) {
  const { valores, errores, enviando, cambiar, enviar } = useFormulario({ ...VACIA, ...item }, validarEmpresa, (datos) =>
    onGuardar(normalizarEmpresa(datos)),
  )

  return (
    <form className="formulario" onSubmit={enviar} noValidate>
      <div className="formulario__rejilla">
        <Input name="nombre" etiqueta="Nombre" ancho value={valores.nombre} onChange={cambiar} error={errores.nombre} />
        <Input name="nit" etiqueta="NIT" inputMode="numeric" placeholder="9001234567" value={valores.nit} onChange={cambiar} error={errores.nit} />
        <Select name="sector" etiqueta="Sector" opciones={OPCIONES_SECTOR} value={valores.sector} onChange={cambiar} error={errores.sector} />
        <Input name="contacto" etiqueta="Persona de contacto" value={valores.contacto} onChange={cambiar} error={errores.contacto} />
        <Input name="telefono" etiqueta="Teléfono" inputMode="numeric" placeholder="3001234567" value={valores.telefono} onChange={cambiar} error={errores.telefono} />
        <Input name="correo" type="email" etiqueta="Correo" ancho value={valores.correo} onChange={cambiar} error={errores.correo} />
        <Casilla name="activa" etiqueta="Empresa activa" checked={valores.activa} onChange={cambiar} />
      </div>
      <AccionesFormulario onCancelar={onCancelar} enviando={enviando} error={errores.general} />
    </form>
  )
}
