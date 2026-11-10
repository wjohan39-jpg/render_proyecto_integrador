"""Descripcion de cada seccion del proyecto: textos, graficas y consultas.

Los archivos que se nombran aqui los genera main.py en data/limpio/ y reportes/.
"""

MODULOS = {
    "prioridades": {
        "nombre": "Prioridades",
        "autor": "Dave",
        "sobretitulo": "ANÁLISIS DE PRIORIDADES",
        "resumen": "Cómo se reparten los niveles de prioridad y cuánto tarda la respuesta en cada uno.",
        "pie": "REPORTE DE PRIORIDADES",
        "prefijo": "prioridades",
        "graficas": [
            ("Filas por nivel", "Cantidad de filas registradas en cada nivel.",
             "Gráfico de barras con la cantidad de filas por nivel."),
            ("Días promedio de respuesta", "Tiempo promedio de respuesta según la prioridad.",
             "Gráfico de barras con los días promedio de respuesta por prioridad."),
            ("Reparto de las prioridades", "Porcentaje de filas que corresponde a cada prioridad.",
             "Gráfico de torta con el reparto de las prioridades."),
        ],
        "consultas": [
            "Prioridades de la más urgente a la menos urgente",
            "Solo las prioridades urgentes (nivel 1 y 2)",
            "Veces que aparece cada nombre",
            "Filas por nivel",
            "Días de respuesta mínimo, promedio y máximo por prioridad",
        ],
    },
    "registros": {
        "nombre": "Registros",
        "autor": "Jeferson",
        "sobretitulo": "ANÁLISIS DE INSCRIPCIONES",
        "resumen": "Una vista clara de la actividad, el ritmo mensual y los retos más concurridos.",
        "pie": "REPORTE DE PARTICIPACIONES",
        "prefijo": "registros",
        "graficas": [
            ("Participaciones por estado", "Distribución de registros según su estado.",
             "Gráfico de barras con la cantidad de participaciones por estado."),
            ("Participaciones por mes", "Evolución mensual de las inscripciones.",
             "Gráfico de líneas con participaciones agrupadas por mes."),
            ("Retos con más participantes", "Los diez retos con mayor cantidad de registros.",
             "Gráfico de barras horizontales con los diez retos más populares."),
        ],
        "consultas": [
            "Participaciones finalizadas",
            "Participaciones repetidas por usuario y reto",
            "Participaciones por estado",
            "Los 10 retos con más participantes",
            "Participaciones por mes",
        ],
    },
    "empresas": {
        "nombre": "Empresas",
        "autor": "Wesly",
        "sobretitulo": "ANÁLISIS DE EMPRESAS",
        "resumen": "Distribución de las empresas por sector y cuántas siguen activas en cada uno.",
        "pie": "REPORTE DE EMPRESAS",
        "prefijo": "empresas",
        "graficas": [
            ("Empresas por sector", "Cantidad de empresas registradas en cada sector.",
             "Gráfico de barras con la cantidad de empresas por sector."),
            ("Activas vs inactivas", "Proporción de empresas activas e inactivas.",
             "Gráfico de torta con empresas activas e inactivas."),
            ("Activas e inactivas por sector", "Estado de las empresas dentro de cada sector.",
             "Gráfico de barras apiladas con empresas activas e inactivas por sector."),
        ],
        "consultas": [
            "Empresas activas",
            "Empresas del sector Tecnología, ordenadas por nombre",
            "Empresas por sector (conteo rápido)",
            "Empresas por sector, de mayor a menor",
            "Empresas activas e inactivas por sector",
        ],
    },
    "retos": {
        "nombre": "Retos",
        "autor": "Diego",
        "sobretitulo": "ANÁLISIS DE RETOS",
        "resumen": "Estado de los retos, cuántos arrancan cada mes y cuánto suelen durar.",
        "pie": "REPORTE DE RETOS",
        "prefijo": "retos",
        "graficas": [
            ("Retos por estado", "Cantidad de retos en cada estado.",
             "Gráfico de barras con la cantidad de retos por estado."),
            ("Retos que empiezan cada mes", "Evolución mensual del inicio de retos.",
             "Gráfico de líneas con los retos que empiezan cada mes."),
            ("Duración de los retos", "Cómo se reparte la duración de los retos.",
             "Histograma con la distribución de la duración de los retos."),
        ],
        "consultas": [
            "Retos en curso",
            "Los 10 retos más largos",
            "Retos por estado",
            "Duración (cantidad, media, mínima y máxima) por estado",
            "Retos que empiezan cada mes",
        ],
    },
}
