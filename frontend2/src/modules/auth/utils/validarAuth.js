import { esCorreoValido, esVacio, MENSAJE_CONTRASENA, POLITICA_CONTRASENA } from '../../core/utils/validaciones'

export function validarLogin({ correo, contrasena }) {
  return {
    correo: esVacio(correo) ? 'Ingresa tu correo.' : !esCorreoValido(correo) ? 'El correo no es válido.' : undefined,
    contrasena: esVacio(contrasena) ? 'Ingresa tu contraseña.' : undefined,
  }
}

export function validarRegistro({ nombre, correo, contrasena, confirmar, rol }) {
  return {
    nombre: nombre.trim().length < 3 ? 'Escribe tu nombre completo.' : undefined,
    correo: esVacio(correo) ? 'Ingresa tu correo.' : !esCorreoValido(correo) ? 'El correo no es válido.' : undefined,
    rol: esVacio(rol) ? 'Selecciona un rol.' : undefined,
    contrasena: !POLITICA_CONTRASENA.test(contrasena) ? MENSAJE_CONTRASENA : undefined,
    confirmar: confirmar !== contrasena ? 'Las contraseñas no coinciden.' : undefined,
  }
}
