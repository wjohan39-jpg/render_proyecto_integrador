import { Building2, ClipboardList, Flag, Trophy, Users } from 'lucide-react'
import { useAuth } from '../../auth/hooks/useAuth'
import Introduccion from '../../core/components/Introduccion'
import EstadoCarga from '../../core/design-system/EstadoCarga'
import { humanizar, plural } from '../../core/utils/formato'
import { useResumen } from '../hooks/useResumen'
import TarjetaModulo from '../components/TarjetaModulo'
import PanelBarras from '../components/PanelBarras'

const mayor = (conteo) => Object.entries(conteo).sort((a, b) => b[1] - a[1])[0]

export default function DashboardPage() {
  const { usuario, esAdministrador } = useAuth()
  const { resumen, cargando, error, recargar } = useResumen(esAdministrador)
  const nombre = usuario.nombre.split(' ')[0]

  return (
    <>
      <Introduccion
        sobretitulo="PANEL GENERAL"
        titulo={`Hola, ${nombre}`}
        resumen="Resumen de los cuatro módulos del proyecto. Entra a cada uno para consultar, crear, modificar o eliminar su información."
        pieIzquierda={`SESIÓN · ${usuario.rol.toUpperCase()}`}
        pieDerecha={resumen ? `${resumen.retos.total} RETOS · ${resumen.registros.total} REGISTROS` : 'CARGANDO…'}
      />

      {!resumen ? (
        <EstadoCarga cargando={cargando} error={error} onReintentar={recargar} textoCarga="Cargando el resumen desde la API…" />
      ) : (
        <>
          <div className="tarjetas">
            <TarjetaModulo
              titulo="Empresas"
              valor={resumen.empresas.total}
              detalle={`${resumen.empresas.activas} activas`}
              autor="WESLY"
              icono={Building2}
              ruta="/empresas"
            />
            <TarjetaModulo
              titulo="Prioridades"
              valor={resumen.prioridades.total}
              detalle={`${resumen.prioridades.porNombre.Alta ?? 0} de nivel alto`}
              autor="DAVE"
              icono={Flag}
              ruta="/prioridades"
            />
            <TarjetaModulo
              titulo="Retos"
              valor={resumen.retos.total}
              detalle={`${resumen.retos.porEstado.COMPLETADA ?? 0} completados`}
              autor="DIEGO"
              icono={Trophy}
              ruta="/retos"
            />
            <TarjetaModulo
              titulo="Registros"
              valor={resumen.registros.total}
              detalle={`${resumen.registros.porEstado.FINALIZADO ?? 0} finalizados`}
              autor="JEFERSON"
              icono={ClipboardList}
              ruta="/registros"
            />
            {resumen.usuarios && (
              <TarjetaModulo
                titulo="Usuarios"
                valor={resumen.usuarios.total}
                detalle={`${resumen.usuarios.activos} activos`}
                autor="ADMINISTRACIÓN"
                icono={Users}
                ruta="/usuarios"
              />
            )}
          </div>

          <div className="resumen">
            <PanelBarras
              titulo="Retos por estado"
              conclusion={resumen.retos.total ? `El estado más común es "${humanizar(mayor(resumen.retos.porEstado)[0])}".` : 'Aún no hay retos.'}
              conteo={resumen.retos.porEstado}
            />
            <PanelBarras
              titulo="Registros por estado"
              conclusion={
                resumen.registros.total
                  ? `${plural(resumen.registros.porEstado.INSCRITO ?? 0, 'registro sigue', 'registros siguen')} en estado inscrito.`
                  : 'Aún no hay registros.'
              }
              conteo={resumen.registros.porEstado}
            />
            <PanelBarras
              titulo="Empresas por sector"
              conclusion={resumen.empresas.total ? `${mayor(resumen.empresas.porSector)[0]} es el sector con más empresas.` : 'Aún no hay empresas.'}
              conteo={resumen.empresas.porSector}
            />
            <PanelBarras titulo="Prioridades por nivel" conclusion="Cantidad de prioridades de cada tipo." conteo={resumen.prioridades.porNombre} />
          </div>
        </>
      )}
    </>
  )
}
