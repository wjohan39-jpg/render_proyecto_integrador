import { useMemo } from 'react'
import PaginaModulo from '../../core/components/PaginaModulo'
import GestionCrud from '../../core/components/GestionCrud'
import { useCrud } from '../../core/hooks/useCrud'
import { indexarPorId } from '../../core/utils/opciones'
import { useAuth } from '../../auth/hooks/useAuth'
import { useRetos } from '../../reto/hooks/useRetos'
import { usuarioService } from '../../usuario/services/usuarioService'
import { useRegistros } from '../hooks/useRegistros'
import { OPCIONES_ESTADO_REGISTRO } from '../lib/constantes'
import RegistroForm from '../components/RegistroForm'
import { crearColumnasRegistro } from '../components/columnasRegistro'

const FILTROS = [{ clave: 'estado', etiqueta: 'Estado', opciones: OPCIONES_ESTADO_REGISTRO, aplicar: (r, v) => r.estado === v }]

export default function RegistrosPage() {
  const { usuario, esAdministrador } = useAuth()
  const crud = useRegistros()
  const retos = useRetos()
  // La lista de usuarios solo la puede leer un administrador (la API responde 403 a los demás).
  const usuarios = useCrud(usuarioService, { activo: esAdministrador })

  const retosPorId = useMemo(() => indexarPorId(retos.items), [retos.items])
  const usuariosPorId = useMemo(() => indexarPorId(usuarios.items), [usuarios.items])
  const columnas = useMemo(() => crearColumnasRegistro({ retosPorId, usuariosPorId }), [retosPorId, usuariosPorId])

  const buscarEn = (r) => [r.observacion, r.estado, r.fecha_registro, retosPorId[r.id_reto]?.nombre, usuariosPorId[r.id_usuario]?.nombre]
  const finalizados = crud.items.filter((r) => r.estado === 'FINALIZADO').length

  return (
    <PaginaModulo
      idReporte="registros"
      intro={{
        sobretitulo: 'GESTIÓN DE INSCRIPCIONES · JEFERSON',
        titulo: 'Registros',
        resumen: 'Cada participación de un usuario en un reto: cuándo se inscribió, en qué estado va y sus observaciones.',
        pieIzquierda: 'MÓDULO DE REGISTROS',
        pieDerecha: crud.cargando ? 'CARGANDO…' : `${crud.items.length} REGISTROS · ${finalizados} FINALIZADOS`,
      }}
    >
      <GestionCrud
        crud={crud}
        entidad={{ singular: 'registro', articulo: 'el' }}
        columnas={columnas}
        buscarEn={buscarEn}
        filtros={FILTROS}
        Formulario={RegistroForm}
        propsFormulario={{ retos: retos.items, usuarios: esAdministrador ? usuarios.items : null, idSesion: usuario.id }}
        describir={(r) => retosPorId[r.id_reto]?.nombre ?? `registro del ${r.fecha_registro}`}
      />
    </PaginaModulo>
  )
}
