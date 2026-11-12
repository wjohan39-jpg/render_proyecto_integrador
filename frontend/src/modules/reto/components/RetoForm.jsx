import { useFormulario } from '../../core/hooks/useFormulario'
import Input from '../../core/design-system/Input'
import Select from '../../core/design-system/Select'
import Textarea from '../../core/design-system/Textarea'
import AccionesFormulario from '../../core/design-system/AccionesFormulario'
import { opcionesRelacion } from '../../core/utils/opciones'
import { describirPrioridad } from '../../prioridad/lib/constantes'
import { OPCIONES_ESTADO_RETO } from '../lib/constantes'
import { normalizarReto, validarReto } from '../utils/validarReto'

const VACIO = {
  nombre: '',
  descripcion: '',
  fecha_inicio: '',
  fecha_fin: '',
  estado: 'PENDIENTE',
  id_empresa: '',
  id_prioridad: '',
  id_categoria: '',
}

// empresas y prioridades llegan desde la página para elegir la relación en una lista.
export default function RetoForm({ item, empresas, prioridades, onGuardar, onCancelar }) {
  const inicial = { ...VACIO, ...Object.fromEntries(Object.entries(item).map(([k, v]) => [k, v ?? ''])) }
  const { valores, errores, enviando, cambiar, enviar } = useFormulario(inicial, validarReto, (datos) => onGuardar(normalizarReto(datos)))

  return (
    <form className="formulario" onSubmit={enviar} noValidate>
      <div className="formulario__rejilla">
        <Input name="nombre" etiqueta="Nombre del reto" ancho value={valores.nombre} onChange={cambiar} error={errores.nombre} />
        <Textarea name="descripcion" etiqueta="Descripción" ancho value={valores.descripcion} onChange={cambiar} error={errores.descripcion} />
        <Input name="fecha_inicio" type="date" etiqueta="Fecha de inicio" value={valores.fecha_inicio} onChange={cambiar} error={errores.fecha_inicio} />
        <Input name="fecha_fin" type="date" etiqueta="Fecha de fin" value={valores.fecha_fin} onChange={cambiar} error={errores.fecha_fin} />
        <Select name="estado" etiqueta="Estado" opciones={OPCIONES_ESTADO_RETO} value={valores.estado} onChange={cambiar} error={errores.estado} />
        <Select
          name="id_prioridad"
          etiqueta="Prioridad"
          placeholder="Sin prioridad"
          opciones={opcionesRelacion(prioridades, describirPrioridad, valores.id_prioridad)}
          value={valores.id_prioridad}
          onChange={cambiar}
          error={errores.id_prioridad}
        />
        <Select
          name="id_empresa"
          etiqueta="Empresa"
          placeholder="Sin empresa"
          ancho
          opciones={opcionesRelacion(empresas, (e) => `${e.nombre} · NIT ${e.nit}`, valores.id_empresa)}
          value={valores.id_empresa}
          onChange={cambiar}
          error={errores.id_empresa}
        />
        <Input
          name="id_categoria"
          etiqueta="ID de categoría"
          ancho
          placeholder="Opcional"
          ayuda="La API no tiene tabla de categorías; se guarda el identificador tal cual."
          value={valores.id_categoria}
          onChange={cambiar}
          error={errores.id_categoria}
        />
      </div>
      <AccionesFormulario onCancelar={onCancelar} enviando={enviando} error={errores.general} />
    </form>
  )
}
