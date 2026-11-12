import { usePeticion } from '../hooks/usePeticion'
import { obtenerReporte } from '../lib/reportesApi'
import EstadoCarga from '../design-system/EstadoCarga'
import TarjetaGrafica from '../design-system/TarjetaGrafica'
import PanelConsultas from './PanelConsultas'

// Vista "Reporte" de un módulo: las gráficas y las consultas que genera main.py.
export default function SeccionReporte({ idModulo }) {
  const { datos: modulo, cargando, error, recargar } = usePeticion(() => obtenerReporte(idModulo), [idModulo])

  if (!modulo) {
    return <EstadoCarga cargando={cargando} error={error} onReintentar={recargar} textoCarga="Cargando el reporte…" />
  }

  return (
    <>
      <p className="panel__nota">
        {modulo.pie} · {modulo.totalRegistros} filas en el CSV limpio · generado por main.py
      </p>
      <section className="galeria" aria-label={`Gráficas de ${modulo.nombre.toLowerCase()}`}>
        {modulo.graficas.map((grafica) => (
          <TarjetaGrafica key={grafica.numero} grafica={grafica} />
        ))}
      </section>
      <PanelConsultas idModulo={idModulo} consultas={modulo.consultas} />
    </>
  )
}
