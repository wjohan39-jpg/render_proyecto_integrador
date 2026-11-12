import { useMemo, useState } from 'react'
import { coincide } from '../utils/formato'

// Búsqueda, filtros y paginación en el navegador sobre la lista que entrega la API.
// buscarEn(item) -> textos donde buscar; filtros: [{ clave, aplicar(item, valor) }]
export function useTablaFiltrada(items, { buscarEn, filtros = [], tamano = 15 }) {
  const [busqueda, setBusquedaInterna] = useState('')
  const [valores, setValores] = useState({})
  const [pagina, setPagina] = useState(1)

  const filtrados = useMemo(
    () =>
      items.filter((item) => {
        const pasaFiltros = filtros.every(({ clave, aplicar }) => !valores[clave] || aplicar(item, valores[clave]))
        const pasaBusqueda = !busqueda.trim() || buscarEn(item).some((texto) => coincide(texto, busqueda))
        return pasaFiltros && pasaBusqueda
      }),
    // buscarEn y filtros son configuración fija de cada módulo
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [items, busqueda, valores],
  )

  const totalPaginas = Math.max(1, Math.ceil(filtrados.length / tamano))
  const paginaActual = Math.min(pagina, totalPaginas)
  const visibles = filtrados.slice((paginaActual - 1) * tamano, paginaActual * tamano)

  const setBusqueda = (texto) => {
    setBusquedaInterna(texto)
    setPagina(1)
  }

  const cambiarFiltro = (clave, valor) => {
    setValores((prev) => ({ ...prev, [clave]: valor }))
    setPagina(1)
  }

  return {
    busqueda,
    setBusqueda,
    valores,
    cambiarFiltro,
    pagina: paginaActual,
    setPagina,
    totalPaginas,
    visibles,
    total: filtrados.length,
  }
}
