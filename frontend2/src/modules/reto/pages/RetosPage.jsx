import { useMemo } from 'react'
import PaginaModulo from '../../core/components/PaginaModulo'
import GestionCrud from '../../core/components/GestionCrud'
import { indexarPorId } from '../../core/utils/opciones'
import { useEmpresas } from '../../empresa/hooks/useEmpresas'
import { usePrioridades } from '../../prioridad/hooks/usePrioridades'
import { useRetos } from '../hooks/useRetos'
import { OPCIONES_ESTADO_RETO } from '../lib/constantes'
import RetoForm from '../components/RetoForm'
import { crearColumnasReto } from '../components/columnasReto'

const FILTROS = [{ clave: 'estado', etiqueta: 'Estado', opciones: OPCIONES_ESTADO_RETO, aplicar: (r, v) => r.estado === v }]

export default function RetosPage() {
  const crud = useRetos()
  const empresas = useEmpresas()
  const prioridades = usePrioridades()

  const empresasPorId = useMemo(() => indexarPorId(empresas.items), [empresas.items])
  const prioridadesPorId = useMemo(() => indexarPorId(prioridades.items), [prioridades.items])
  const columnas = useMemo(() => crearColumnasReto({ empresasPorId, prioridadesPorId }), [empresasPorId, prioridadesPorId])

  const buscarEn = (r) => [r.nombre, r.descripcion, r.estado, empresasPorId[r.id_empresa]?.nombre]
  const enCurso = crud.items.filter((r) => r.estado === 'EN_PROGRESO' || r.estado === 'EN_CURSO').length

  return (
    <PaginaModulo
      idReporte="retos"
      intro={{
        sobretitulo: 'GESTIÓN DE RETOS · DIEGO',
        titulo: 'Retos',
        resumen: 'Desafíos que proponen las empresas, con sus fechas, estado, empresa y prioridad.',
        pieIzquierda: 'MÓDULO DE RETOS',
        pieDerecha: crud.cargando ? 'CARGANDO…' : `${crud.items.length} RETOS · ${enCurso} EN CURSO`,
      }}
    >
      <GestionCrud
        crud={crud}
        entidad={{ singular: 'reto', articulo: 'el' }}
        columnas={columnas}
        buscarEn={buscarEn}
        filtros={FILTROS}
        Formulario={RetoForm}
        propsFormulario={{ empresas: empresas.items, prioridades: prioridades.items }}
        describir={(r) => r.nombre}
      />
    </PaginaModulo>
  )
}
