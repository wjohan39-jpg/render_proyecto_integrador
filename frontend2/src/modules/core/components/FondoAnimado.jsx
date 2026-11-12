import { useEffect, useRef } from 'react'

// Colores Cesde en RGB: magenta, morado y naranja.
const COLORES = ['219, 39, 113', '101, 45, 144', '255, 93, 49']
const DISTANCIA_ENLACE = 150

const azar = (min, max) => min + Math.random() * (max - min)

// Traza un polígono regular (o un círculo si lados = 0) centrado en la figura.
function trazarFigura(ctx, f, desplazamientoY) {
  ctx.beginPath()
  if (f.lados === 0) {
    ctx.arc(f.x, f.y + desplazamientoY, f.tamano / 2, 0, Math.PI * 2)
    return
  }
  for (let i = 0; i <= f.lados; i++) {
    const a = f.angulo + (i / f.lados) * Math.PI * 2
    const x = f.x + Math.cos(a) * (f.tamano / 2)
    const y = f.y + desplazamientoY + Math.sin(a) * (f.tamano / 2)
    if (i === 0) ctx.moveTo(x, y)
    else ctx.lineTo(x, y)
  }
  ctx.closePath()
}

// Fondo decorativo del visor: aurora con los colores de Cesde, rejilla en perspectiva,
// figuras geométricas flotantes y una red de puntos en movimiento.
// No recibe clics ni lo leen los lectores de pantalla.
export default function FondoAnimado() {
  const lienzoRef = useRef(null)

  useEffect(() => {
    const lienzo = lienzoRef.current
    const ctx = lienzo?.getContext('2d')
    if (!lienzo || !ctx) return

    const reducirMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let puntos = []
    let figuras = []
    let ancho = 0
    let alto = 0
    let animacion = 0

    const crear = () => {
      const escala = window.devicePixelRatio || 1
      ancho = window.innerWidth
      alto = window.innerHeight
      lienzo.width = ancho * escala
      lienzo.height = alto * escala
      ctx.setTransform(escala, 0, 0, escala, 0, 0)

      const area = ancho * alto
      puntos = Array.from({ length: Math.min(55, Math.round(area / 26000)) }, (_, i) => ({
        x: Math.random() * ancho,
        y: Math.random() * alto,
        vx: azar(-0.6, 0.6),
        vy: azar(-0.6, 0.6),
        color: COLORES[i % 2],
      }))

      const tiposLados = [0, 3, 4, 6]
      figuras = Array.from({ length: Math.max(6, Math.min(16, Math.round(area / 80000))) }, (_, i) => ({
        x: Math.random() * ancho,
        y: Math.random() * alto,
        vx: azar(-0.7, 0.7) || 0.4,
        vy: azar(-0.5, 0.5) || -0.3,
        tamano: azar(26, 80),
        angulo: Math.random() * Math.PI * 2,
        giro: azar(-0.012, 0.012),
        lados: tiposLados[i % tiposLados.length],
        color: COLORES[i % COLORES.length],
        relleno: i % 3 === 0,
        fase: Math.random() * Math.PI * 2,
      }))
    }

    const dibujar = (tiempo) => {
      ctx.clearRect(0, 0, ancho, alto)

      for (const f of figuras) {
        trazarFigura(ctx, f, Math.sin(tiempo / 1400 + f.fase) * 10)
        if (f.relleno) {
          ctx.fillStyle = `rgba(${f.color}, 0.08)`
          ctx.fill()
        }
        ctx.strokeStyle = `rgba(${f.color}, 0.38)`
        ctx.lineWidth = 1.5
        ctx.stroke()
      }

      for (let i = 0; i < puntos.length; i++) {
        const a = puntos[i]
        for (let j = i + 1; j < puntos.length; j++) {
          const b = puntos[j]
          const distancia = Math.hypot(a.x - b.x, a.y - b.y)
          if (distancia < DISTANCIA_ENLACE) {
            ctx.strokeStyle = `rgba(${a.color}, ${0.2 * (1 - distancia / DISTANCIA_ENLACE)})`
            ctx.lineWidth = 1
            ctx.beginPath()
            ctx.moveTo(a.x, a.y)
            ctx.lineTo(b.x, b.y)
            ctx.stroke()
          }
        }
        ctx.fillStyle = `rgba(${a.color}, 0.55)`
        ctx.beginPath()
        ctx.arc(a.x, a.y, 1.8, 0, Math.PI * 2)
        ctx.fill()
      }
    }

    const mover = (tiempo) => {
      for (const p of puntos) {
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > ancho) p.vx *= -1
        if (p.y < 0 || p.y > alto) p.vy *= -1
      }
      for (const f of figuras) {
        f.x += f.vx
        f.y += f.vy
        f.angulo += f.giro
        // Al salir por un borde, la figura reaparece por el contrario
        const margen = f.tamano
        if (f.x < -margen) f.x = ancho + margen
        if (f.x > ancho + margen) f.x = -margen
        if (f.y < -margen) f.y = alto + margen
        if (f.y > alto + margen) f.y = -margen
      }
      dibujar(tiempo)
      animacion = requestAnimationFrame(mover)
    }

    const alRedimensionar = () => {
      crear()
      if (reducirMovimiento) dibujar(0)
    }

    crear()
    if (reducirMovimiento) dibujar(0)
    else animacion = requestAnimationFrame(mover)
    window.addEventListener('resize', alRedimensionar)

    return () => {
      cancelAnimationFrame(animacion)
      window.removeEventListener('resize', alRedimensionar)
    }
  }, [])

  return (
    <div className="fondo" aria-hidden="true">
      <div className="fondo__aurora">
        <span />
        <span />
        <span />
      </div>
      <div className="fondo__rejilla" />
      <canvas ref={lienzoRef} className="fondo__red" />
    </div>
  )
}
