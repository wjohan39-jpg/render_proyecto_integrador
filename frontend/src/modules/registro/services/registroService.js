import { crearCrudService } from '../../core/lib/crudService'

// GET/POST /api/registros · GET/PUT/DELETE /api/registros/{id}
export const registroService = crearCrudService('registros')
