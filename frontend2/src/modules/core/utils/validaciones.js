export const esCorreoValido = (correo) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(`${correo ?? ''}`.trim())

export const esVacio = (valor) => valor === null || valor === undefined || `${valor}`.trim() === ''

export const soloDigitos = (texto) => `${texto ?? ''}`.replace(/\D/g, '')

// Mínimo 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial (igual que la API).
export const POLITICA_CONTRASENA = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/
export const MENSAJE_CONTRASENA = 'Mínimo 8 caracteres, con mayúscula, minúscula, número y símbolo.'
