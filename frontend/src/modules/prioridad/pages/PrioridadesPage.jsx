import PaginaModulo from '../../core/components/PaginaModulo'
import GestionCrud from '../../core/components/GestionCrud'
import { usePrioridades } from '../hooks/usePrioridades'
import { NIVELES_PRIORIDAD } from '../lib/constantes'
import PrioridadForm from '../components/PrioridadForm'
import { COLUMNAS_PRIORIDAD } from '../components/columnasPrioridad'

const FILTROS = [
  {
    clave: 'nombre',
    etiqueta: 'Prioridad',
    opciones: NIVELES_PRIORIDAD.map((p) => ({ valor: p.nombre, texto: p.nombre })),
    aplicar: (p, v) => p.nombre === v,
  },
]

const buscarEn = (p) => [p.nombre, String(p.nivel), String(p.dias_max_respuesta), p.id]

export default function PrioridadesPage() {
  const crud = usePrioridades()
  const altas = crud.items.filter((p) => p.nombre === 'Alta').length

  return (
    <PaginaModulo
      idReporte="prioridades"
      intro={{
        sobretitulo: 'GESTIÓN DE PRIORIDADES · DAVE',
        titulo: 'Prioridades',
        resumen: 'Niveles de urgencia de los retos y el plazo máximo de respuesta de cada uno.',
        pieIzquierda: 'MÓDULO DE PRIORIDADES',
        pieDerecha: crud.cargando ? 'CARGANDO…' : `${crud.items.length} PRIORIDADES · ${altas} ALTAS`,
      }}
    >
      <GestionCrud
        crud={crud}
        entidad={{ singular: 'prioridad', articulo: 'la' }}
        columnas={COLUMNAS_PRIORIDAD}
        buscarEn={buscarEn}
        filtros={FILTROS}
        Formulario={PrioridadForm}
        describir={(p) => `${p.nombre} (${p.dias_max_respuesta} días)`}
      />
    </PaginaModulo>
  )
}
