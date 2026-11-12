import { useMemo } from 'react'
import PaginaModulo from '../../core/components/PaginaModulo'
import GestionCrud from '../../core/components/GestionCrud'
import { useAuth } from '../../auth/hooks/useAuth'
import { useUsuarios } from '../hooks/useUsuarios'
import { OPCIONES_ESTADO, OPCIONES_ROL } from '../lib/constantes'
import UsuarioForm from '../components/UsuarioForm'
import { crearColumnasUsuario } from '../components/columnasUsuario'

const FILTROS = [
  { clave: 'rol', etiqueta: 'Rol', opciones: OPCIONES_ROL, aplicar: (u, v) => u.rol === v },
  { clave: 'estado', etiqueta: 'Estado', opciones: OPCIONES_ESTADO, aplicar: (u, v) => (v === 'activos' ? u.activo : !u.activo) },
]

const buscarEn = (u) => [u.nombre, u.correo, u.rol]

export default function UsuariosPage() {
  const { usuario: sesion } = useAuth()
  const crud = useUsuarios()
  const columnas = useMemo(() => crearColumnasUsuario(sesion.id), [sesion.id])
  const activos = crud.items.filter((u) => u.activo).length

  return (
    <PaginaModulo
      intro={{
        sobretitulo: 'ADMINISTRACIÓN',
        titulo: 'Usuarios',
        resumen: 'Personas con acceso a la plataforma, su rol y si pueden iniciar sesión. Solo para administradores.',
        pieIzquierda: 'MÓDULO DE USUARIOS',
        pieDerecha: crud.cargando ? 'CARGANDO…' : `${crud.items.length} USUARIOS · ${activos} ACTIVOS`,
      }}
    >
      <GestionCrud
        crud={crud}
        entidad={{ singular: 'usuario', articulo: 'el' }}
        columnas={columnas}
        buscarEn={buscarEn}
        filtros={FILTROS}
        Formulario={UsuarioForm}
        describir={(u) => u.nombre}
        validarEliminar={(u) => (u.id === sesion.id ? 'No puedes eliminar tu propia cuenta mientras tienes la sesión abierta.' : null)}
      />
    </PaginaModulo>
  )
}
