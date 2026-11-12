import { useCrud } from '../../core/hooks/useCrud'
import { empresaService } from '../services/empresaService'

export function useEmpresas() {
  return useCrud(empresaService)
}
