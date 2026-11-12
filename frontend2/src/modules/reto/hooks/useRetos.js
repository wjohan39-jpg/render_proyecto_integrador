import { useCrud } from '../../core/hooks/useCrud'
import { retoService } from '../services/retoService'

export function useRetos() {
  return useCrud(retoService)
}
