"""Proyecto integrador unificado: Dave (prioridades), Jeferson (registros),
Wesly (empresas) y Diego (retos).

Ejecuta las cinco etapas en orden (simulacion, exportacion, limpieza,
consultas y graficacion) y, dentro de cada etapa, el trabajo de los cuatro
desarrolladores. Reune en un solo archivo lo que hacia el main.py de cada uno.

    python main.py                      # todas las etapas
    python main.py --etapa limpieza     # solo una etapa
"""
import argparse
import os
import sys
from importlib import import_module

# Raiz del proyecto: la carpeta donde esta este main.py
RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA_NOTEBOOK = os.path.join(RAIZ, "src", "notebook")

# Dave y Wesly usan rutas relativas ("data/crudo", "reportes"): se trabaja desde la raiz.
os.chdir(RAIZ)

# Rutas de importacion que usaba cada desarrollador:
#  - raiz            -> "src.notebook...."         (Dave, Jeferson)
#  - src/notebook    -> "simulacion.simular_..."   (Wesly)
#  - cada subcarpeta -> "simular_reto", ...        (Diego)
for carpeta in ["simulacion", "exportacion", "limpieza", "consultas", "graficacion"]:
    sys.path.insert(0, os.path.join(CARPETA_NOTEBOOK, carpeta))
sys.path.insert(0, CARPETA_NOTEBOOK)
sys.path.insert(0, RAIZ)

# --- Dave (prioridades) ---
dave_simulacion = import_module("src.notebook.simulacion.simular_prioridades")
dave_exportacion = import_module("src.notebook.exportacion.exportar_prioridades")
dave_limpieza = import_module("src.notebook.limpieza.limpiar_prioridad")
dave_consultas = import_module("src.notebook.consultas.consultar_prioridades")
dave_graficacion = import_module("src.notebook.graficacion.graficar_prioridades")

# --- Jeferson (registros) ---
from src.notebook.consultas.consultas_registros import ejecutar_consultas
from src.notebook.exportacion.exportar_registros import exportar_registros
from src.notebook.graficacion.reporte_registros import generar_reporte
from src.notebook.limpieza.limpiar_registros import limpiar_registros

# --- Wesly (empresas) ---
from simulacion.simular_empresas import generar_empresas
from exportacion.exportar_empresas import exportar_empresas
from limpieza.limpiar_empresas import leer_csv, diagnostico, limpiar
from consultas.consultas_empresas import (
    cargar_datos,
    consulta_1_activas,
    consulta_2_sector_ordenado,
    consulta_3_conteo_sector,
    consulta_4_groupby_sector,
    consulta_5_groupby_doble,
)
from graficacion import reporte_empresas as reporte

# --- Diego (retos) ---
import simular_reto
import exportar_reto
import limpiar_reto
import consultar_reto
import graficar_reto

CARPETA_CRUDO = os.path.join(RAIZ, "data", "crudo")
CARPETA_LIMPIO = os.path.join(RAIZ, "data", "limpio")
CARPETA_REPORTES = os.path.join(RAIZ, "reportes")


def titulo(texto):
    print("\n" + "-" * 50)
    print(texto)
    print("-" * 50)


# ======================= 1. SIMULACION =======================
def etapa_simulacion():
    titulo("Dave: simular_prioridades.py")
    df = dave_simulacion.generar_prioridades()
    print("Forma:", df.shape)
    print(df.head())
    print("\nNulos por columna:")
    print(df.isna().sum())
    print("Duplicados exactos:", df.duplicated().sum())

    # Jeferson no tenia etapa de simulacion propia: exportar_registros() genera los datos.

    titulo("Wesly: simular_empresas.py")
    df = generar_empresas()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())

    titulo("Diego: simular_reto.py")
    df = simular_reto.generar_retos(500)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
    print("Duplicados exactos:", df.duplicated().sum())


# ======================= 2. EXPORTACION =======================
def etapa_exportacion():
    titulo("Dave: exportar_prioridades.py")
    dave_exportacion.exportar()

    titulo("Jeferson: exportar_registros.py")
    exportar_registros()

    titulo("Wesly: exportar_empresas.py")
    exportar_empresas(CARPETA_CRUDO)

    titulo("Diego: exportar_reto.py")
    exportar_reto.exportar_retos(500)


# ======================= 3. LIMPIEZA =======================
def etapa_limpieza():
    titulo("Dave: limpiar_prioridad.py")
    dave_limpieza.main()

    titulo("Jeferson: limpiar_registros.py")
    limpiar_registros()

    titulo("Wesly: limpiar_empresas.py")
    ruta_entrada = os.path.join(CARPETA_CRUDO, "empresas_sucio.csv")
    df = leer_csv(ruta_entrada)
    filas_antes = len(df)
    diagnostico(df, "DIAGNOSTICO ANTES DE LIMPIAR")
    df = limpiar(df)
    diagnostico(df, "DIAGNOSTICO DESPUES DE LIMPIAR")
    print(f"\nFilas antes: {filas_antes} | despues: {len(df)} | eliminadas: {filas_antes - len(df)}")
    os.makedirs(CARPETA_LIMPIO, exist_ok=True)
    ruta_salida = os.path.join(CARPETA_LIMPIO, "empresas_limpio.csv")
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo guardado en: {ruta_salida}")

    titulo("Diego: limpiar_reto.py")
    limpiar_reto.limpiar_retos()


# ======================= 4. CONSULTAS =======================
def etapa_consultas():
    titulo("Dave: consultar_prioridades.py")
    dave_consultas.main()

    titulo("Jeferson: consultas_registros.py")
    ejecutar_consultas()

    titulo("Wesly: consultas_empresas.py")
    df = cargar_datos(os.path.join(CARPETA_LIMPIO, "empresas_limpio.csv"))
    consultas = [
        consulta_1_activas,
        consulta_2_sector_ordenado,
        consulta_3_conteo_sector,
        consulta_4_groupby_sector,
        consulta_5_groupby_doble,
    ]
    for n, consulta in enumerate(consultas, start=1):
        resultado = consulta(df)
        ruta = os.path.join(CARPETA_LIMPIO, f"empresas_consulta_{n}.csv")
        resultado.to_csv(ruta, index=False)
        print(f"-> Guardado: {ruta}")

    titulo("Diego: consultar_reto.py")
    consultar_reto.consultar_retos()


# ======================= 5. GRAFICACION =======================
def etapa_graficacion():
    titulo("Dave: graficar_prioridades.py")
    dave_graficacion.main()

    titulo("Jeferson: reporte_registros.py")
    generar_reporte()

    titulo("Wesly: reporte_empresas.py")
    reporte.CARPETA_SALIDA = CARPETA_REPORTES
    df = reporte.leer_datos(os.path.join(CARPETA_LIMPIO, "empresas_limpio.csv"))
    df = reporte.preparar_datos(df)
    correos_invalidos = reporte.contar_correos_invalidos(df)
    print("Graficas generadas:")
    for ruta in (reporte.grafica_1_por_sector(df),
                 reporte.grafica_2_activas_inactivas(df),
                 reporte.grafica_3_apiladas(df)):
        print(f"  - {ruta}")
    reporte.imprimir_conclusiones(df, correos_invalidos)

    titulo("Diego: graficar_reto.py")
    graficar_reto.graficar_retos()


ETAPAS = {
    "simulacion": ("1. SIMULACION", etapa_simulacion),
    "exportacion": ("2. EXPORTACION", etapa_exportacion),
    "limpieza": ("3. LIMPIEZA", etapa_limpieza),
    "consultas": ("4. CONSULTAS", etapa_consultas),
    "graficacion": ("5. GRAFICACION", etapa_graficacion),
}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Proyecto integrador unificado.")
    parser.add_argument(
        "--etapa",
        choices=("todo", *ETAPAS),
        default="todo",
        help="etapa que se ejecuta (por defecto: todo)",
    )
    args = parser.parse_args(argv)
    # Algunos modulos (Dave) leen sys.argv como ruta de entrada: se limpia para que
    # "--etapa ..." no se confunda con una ruta.
    sys.argv = sys.argv[:1]

    etapas = ETAPAS if args.etapa == "todo" else {args.etapa: ETAPAS[args.etapa]}
    try:
        for nombre, (texto, ejecutar) in etapas.items():
            print("\n" + "=" * 50)
            print(f"=== {texto} ===")
            print("=" * 50)
            ejecutar()
    except FileNotFoundError as error:
        parser.exit(status=1, message=f"Error: {error}\n")

    print("\nProceso finalizado. Revisa data/ y reportes/.")


if __name__ == "__main__":
    main()
