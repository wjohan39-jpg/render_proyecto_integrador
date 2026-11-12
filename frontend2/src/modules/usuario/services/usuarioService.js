import { crearCrudService } from '../../core/lib/crudService'

// GET/POST /api/usuarios · GET/PUT/DELETE /api/usuarios/{id}  (solo administradores)
export const usuarioService = crearCrudService('usuarios')
