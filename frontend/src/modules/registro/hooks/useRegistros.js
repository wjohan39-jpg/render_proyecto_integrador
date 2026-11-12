import { useCrud } from '../../core/hooks/useCrud'
import { registroService } from '../services/registroService'

export function useRegistros() {
  return useCrud(registroService)
}
