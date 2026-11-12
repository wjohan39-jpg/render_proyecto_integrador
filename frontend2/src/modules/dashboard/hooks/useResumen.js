import { useMemo } from 'react'
import { usePeticion } from '../../core/hooks/usePeticion'
import { empresaService } from '../../empresa/services/empresaService'
import { prioridadService } from '../../prioridad/services/prioridadService'
import { retoService } from '../../reto/services/retoService'
import { registroService } from '../../registro/services/registroService'
import { usuarioService } from '../../usuario/services/usuarioService'

const contarPor = (lista, campo) =>
  lista.reduce((acc, item) => {
    acc[item[campo]] = (acc[item[campo]] ?? 0) + 1
    return acc
  }, {})

// Reúne los datos de todos los módulos (una petición por recurso, en paralelo).
export function useResumen(incluirUsuarios) {
  const peticion = usePeticion(
    () =>
      Promise.all([
        empresaService.obtenerTodos(),
        prioridadService.obtenerTodos(),
        retoService.obtenerTodos(),
        registroService.obtenerTodos(),
        incluirUsuarios ? usuarioService.obtenerTodos() : Promise.resolve(null),
      ]),
    [incluirUsuarios],
  )

  const resumen = useMemo(() => {
    if (!peticion.datos) return null
    const [empresas, prioridades, retos, registros, usuarios] = peticion.datos
    return {
      empresas: { total: empresas.length, activas: empresas.filter((e) => e.activa).length, porSector: contarPor(empresas, 'sector') },
      prioridades: { total: prioridades.length, porNombre: contarPor(prioridades, 'nombre') },
      retos: { total: retos.length, porEstado: contarPor(retos, 'estado') },
      registros: { total: registros.length, porEstado: contarPor(registros, 'estado') },
      usuarios: usuarios && { total: usuarios.length, activos: usuarios.filter((u) => u.activo).length },
    }
  }, [peticion.datos])

  return { resumen, cargando: peticion.cargando, error: peticion.error, recargar: peticion.recargar }
}
