import { esCorreoValido, esVacio, soloDigitos } from '../../core/utils/validaciones'
import { limpiar } from '../../core/utils/formato'

// Mismas reglas que la API: NIT de 8 a 10 dígitos y teléfono de 7 a 12 dígitos (puede incluir el 57).
export function validarEmpresa(valores) {
  const nit = soloDigitos(valores.nit)
  const telefono = soloDigitos(valores.telefono)

  return {
    nombre: limpiar(valores.nombre).length < 3 ? 'El nombre debe tener al menos 3 caracteres.' : undefined,
    nit: nit.length < 8 || nit.length > 10 ? 'El NIT debe tener entre 8 y 10 dígitos.' : undefined,
    sector: esVacio(valores.sector) ? 'Selecciona un sector.' : undefined,
    contacto: limpiar(valores.contacto).length < 3 ? 'Escribe el nombre del contacto.' : undefined,
    correo: !esCorreoValido(valores.correo) ? 'Escribe un correo válido (debe tener @).' : undefined,
    telefono: telefono.length < 7 || telefono.length > 12 ? 'El teléfono debe tener entre 7 y 12 dígitos.' : undefined,
  }
}

// Limpia los datos antes de enviarlos a la API.
export function normalizarEmpresa(valores) {
  return {
    nombre: limpiar(valores.nombre),
    nit: soloDigitos(valores.nit),
    sector: valores.sector,
    contacto: limpiar(valores.contacto),
    correo: limpiar(valores.correo).toLowerCase(),
    telefono: soloDigitos(valores.telefono),
    activa: Boolean(valores.activa),
  }
}
