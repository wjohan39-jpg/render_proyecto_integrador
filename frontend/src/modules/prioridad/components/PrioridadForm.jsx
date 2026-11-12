import { useFormulario } from '../../core/hooks/useFormulario'
import Input from '../../core/design-system/Input'
import Select from '../../core/design-system/Select'
import AccionesFormulario from '../../core/design-system/AccionesFormulario'
import { DIAS_MAXIMOS, NIVELES_PRIORIDAD, OPCIONES_PRIORIDAD } from '../lib/constantes'
import { normalizarPrioridad, validarPrioridad } from '../utils/validarPrioridad'

const VACIA = { nombre: '', dias_max_respuesta: '' }

export default function PrioridadForm({ item, onGuardar, onCancelar }) {
  const { valores, errores, enviando, cambiar, asignar, enviar } = useFormulario({ ...VACIA, ...item }, validarPrioridad, (datos) =>
    onGuardar(normalizarPrioridad(datos)),
  )
  const nivel = NIVELES_PRIORIDAD.find((p) => p.nombre === valores.nombre)

  // Al elegir la prioridad se sugieren los días de respuesta de simular_prioridades.py
  const cambiarNombre = (e) => {
    cambiar(e)
    const sugerida = NIVELES_PRIORIDAD.find((p) => p.nombre === e.target.value)
    if (sugerida) asignar({ dias_max_respuesta: String(sugerida.dias) })
  }

  return (
    <form className="formulario" onSubmit={enviar} noValidate>
      <div className="formulario__rejilla">
        <Select name="nombre" etiqueta="Prioridad" opciones={OPCIONES_PRIORIDAD} value={valores.nombre} onChange={cambiarNombre} error={errores.nombre} />
        <Input name="nivel" etiqueta="Nivel" value={nivel ? nivel.nivel : '—'} readOnly ayuda="Se asigna según la prioridad." />
        <Input
          name="dias_max_respuesta"
          type="number"
          min="1"
          max={DIAS_MAXIMOS}
          etiqueta="Días máximos de respuesta"
          ancho
          value={valores.dias_max_respuesta}
          onChange={cambiar}
          error={errores.dias_max_respuesta}
        />
      </div>
      <AccionesFormulario onCancelar={onCancelar} enviando={enviando} error={errores.general} />
    </form>
  )
}
