import { esCorreoValido, esVacio, MENSAJE_CONTRASENA, POLITICA_CONTRASENA } from '../../core/utils/validaciones'
import { limpiar } from '../../core/utils/formato'

// esNuevo: al crear, la contraseña es obligatoria; al editar, solo se valida si se escribe una nueva.
export function validarUsuario(valores, esNuevo) {
  const contrasena = valores.contrasena ?? ''
  const cambiaContrasena = esNuevo || contrasena !== ''

  return {
    nombre: limpiar(valores.nombre).length < 3 ? 'Escribe el nombre completo (mínimo 3 caracteres).' : undefined,
    correo: !esCorreoValido(valores.correo) ? 'Escribe un correo válido.' : undefined,
    rol: esVacio(valores.rol) ? 'Selecciona un rol.' : undefined,
    contrasena: cambiaContrasena && !POLITICA_CONTRASENA.test(contrasena) ? MENSAJE_CONTRASENA : undefined,
    confirmar: cambiaContrasena && valores.confirmar !== contrasena ? 'Las contraseñas no coinciden.' : undefined,
  }
}

// Limpia los datos antes de enviarlos. La contraseña solo se envía si se escribió.
export function normalizarUsuario(valores) {
  const datos = {
    nombre: limpiar(valores.nombre),
    correo: limpiar(valores.correo).toLowerCase(),
    rol: valores.rol,
    activo: Boolean(valores.activo),
  }
  if (valores.contrasena) datos.contrasena = valores.contrasena
  return datos
}
