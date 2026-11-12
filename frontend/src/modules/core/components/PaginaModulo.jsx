import { useSearchParams } from 'react-router-dom'
import { BarChart3, Table2 } from 'lucide-react'
import Boton from '../design-system/Boton'
import Introduccion from './Introduccion'
import SeccionReporte from './SeccionReporte'

// Página de un módulo: introducción + sub-pestañas "Gestión" (CRUD) y "Reporte" (gráficas y consultas).
// La vista elegida queda en la URL (?vista=reporte) para poder compartirla o recargar.
export default function PaginaModulo({ intro, idReporte, children }) {
  const [parametros, setParametros] = useSearchParams()
  const vista = idReporte && parametros.get('vista') === 'reporte' ? 'reporte' : 'gestion'

  const cambiarVista = (nueva) => setParametros(nueva === 'reporte' ? { vista: 'reporte' } : {}, { replace: true })

  return (
    <>
      <Introduccion {...intro} />
      {idReporte && (
        <div className="vistas" role="group" aria-label="Vista del módulo">
          <Boton icono={Table2} activo={vista === 'gestion'} onClick={() => cambiarVista('gestion')}>
            Gestión (CRUD)
          </Boton>
          <Boton icono={BarChart3} activo={vista === 'reporte'} onClick={() => cambiarVista('reporte')}>
            Reporte
          </Boton>
        </div>
      )}
      {vista === 'reporte' ? <SeccionReporte idModulo={idReporte} /> : children}
    </>
  )
}
