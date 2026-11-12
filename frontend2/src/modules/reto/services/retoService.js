import { crearCrudService } from '../../core/lib/crudService'

// GET/POST /api/retos · GET/PUT/DELETE /api/retos/{id}
export const retoService = crearCrudService('retos')
