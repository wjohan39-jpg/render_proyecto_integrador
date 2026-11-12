import { useState } from 'react'
import { usePeticion } from '../hooks/usePeticion'
import { obtenerConsulta } from '../lib/reportesApi'
import Boton from '../design-system/Boton'
import EstadoCarga from '../design-system/EstadoCarga'
import TablaDatos from '../design-system/TablaDatos'

const FILAS_VISIBLES = 50

// Las cinco consultas de cada sección (resultados de main.py), una a la vez.
export default function PanelConsultas({ idModulo, consultas }) {
  const [numero, setNumero] = useState(1)
  const { datos, cargando, error, recargar } = usePeticion(() => obtenerConsulta(idModulo, numero), [idModulo, numero])
  const actual = consultas.find((c) => c.numero === numero)

  return (
    <section className="panel" aria-labelledby="titulo-consultas">
      <header className="panel__encabezado">
        <h2 id="titulo-consultas">Consultas</h2>
        <div className="panel__acciones">
          {consultas.map((consulta) => (
            <Boton key={consulta.numero} activo={consulta.numero === numero} onClick={() => setNumero(consulta.numero)} title={consulta.titulo}>
              {consulta.numero}
            </Boton>
          ))}
        </div>
      </header>
      <p className="panel__subtitulo">{actual?.titulo}</p>

      <EstadoCarga cargando={cargando} error={error} textoCarga="Consultando la API…" onReintentar={recargar} />
      {datos && !cargando && (
        <>
          <TablaDatos columnas={datos.columnas} filas={datos.filas.slice(0, FILAS_VISIBLES)} titulo={datos.titulo} />
          <p className="panel__nota">
            {datos.total > FILAS_VISIBLES ? `Mostrando ${FILAS_VISIBLES} de ${datos.total} filas.` : `${datos.total} filas.`}
          </p>
        </>
      )}
    </section>
  )
}
