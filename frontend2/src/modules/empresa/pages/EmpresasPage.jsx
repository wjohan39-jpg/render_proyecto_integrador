import PaginaModulo from '../../core/components/PaginaModulo'
import GestionCrud from '../../core/components/GestionCrud'
import { useEmpresas } from '../hooks/useEmpresas'
import { OPCIONES_ESTADO, OPCIONES_SECTOR } from '../lib/constantes'
import EmpresaForm from '../components/EmpresaForm'
import { COLUMNAS_EMPRESA } from '../components/columnasEmpresa'

const FILTROS = [
  { clave: 'sector', etiqueta: 'Sector', opciones: OPCIONES_SECTOR, aplicar: (e, v) => e.sector === v },
  { clave: 'estado', etiqueta: 'Estado', opciones: OPCIONES_ESTADO, aplicar: (e, v) => (v === 'activas' ? e.activa : !e.activa) },
]

const buscarEn = (e) => [e.nombre, e.nit, e.contacto, e.correo, e.telefono]

export default function EmpresasPage() {
  const crud = useEmpresas()
  const activas = crud.items.filter((e) => e.activa).length

  return (
    <PaginaModulo
      idReporte="empresas"
      intro={{
        sobretitulo: 'GESTIÓN DE EMPRESAS · WESLY',
        titulo: 'Empresas',
        resumen: 'Organizaciones aliadas que proponen retos. Busca, filtra, crea, modifica o elimina empresas.',
        pieIzquierda: 'MÓDULO DE EMPRESAS',
        pieDerecha: crud.cargando ? 'CARGANDO…' : `${crud.items.length} EMPRESAS · ${activas} ACTIVAS`,
      }}
    >
      <GestionCrud
        crud={crud}
        entidad={{ singular: 'empresa', articulo: 'la' }}
        columnas={COLUMNAS_EMPRESA}
        buscarEn={buscarEn}
        filtros={FILTROS}
        Formulario={EmpresaForm}
        describir={(e) => e.nombre}
      />
    </PaginaModulo>
  )
}
