import { crearCrudService } from '../../core/lib/crudService'

// GET/POST /api/empresas · GET/PUT/DELETE /api/empresas/{id}
export const empresaService = crearCrudService('empresas')
