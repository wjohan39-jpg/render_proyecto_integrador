import { useCrud } from '../../core/hooks/useCrud'
import { prioridadService } from '../services/prioridadService'

export function usePrioridades() {
  return useCrud(prioridadService)
}
