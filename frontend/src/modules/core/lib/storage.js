// Lectura y escritura segura en localStorage (los datos se guardan como JSON).
export function leer(clave, porDefecto = null) {
  try {
    const valor = localStorage.getItem(clave)
    return valor === null ? porDefecto : JSON.parse(valor)
  } catch {
    return porDefecto
  }
}

export function guardar(clave, valor) {
  try {
    localStorage.setItem(clave, JSON.stringify(valor))
  } catch {
    // almacenamiento no disponible
  }
}

export function borrar(clave) {
  try {
    localStorage.removeItem(clave)
  } catch {
    // almacenamiento no disponible
  }
}
