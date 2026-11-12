import { Building2, ClipboardList, Flag, LayoutDashboard, Trophy, Users } from 'lucide-react'

export const INICIO = '/dashboard'

// Pestañas de la navegación principal. "detalle" es el texto pequeño en mono (como en el visor).
export const PESTANAS = [
  { ruta: INICIO, texto: 'Inicio', detalle: 'Panel general', icono: LayoutDashboard },
  { ruta: '/empresas', texto: 'Empresas', detalle: 'Wesly', icono: Building2 },
  { ruta: '/prioridades', texto: 'Prioridades', detalle: 'Dave', icono: Flag },
  { ruta: '/retos', texto: 'Retos', detalle: 'Diego', icono: Trophy },
  { ruta: '/registros', texto: 'Registros', detalle: 'Jeferson', icono: ClipboardList },
  { ruta: '/usuarios', texto: 'Usuarios', detalle: 'Administración', icono: Users, soloAdmin: true },
]
