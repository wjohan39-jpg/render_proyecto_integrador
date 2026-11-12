import { useCrud } from '../../core/hooks/useCrud'
import { usuarioService } from '../services/usuarioService'

export function useUsuarios() {
  return useCrud(usuarioService)
}
