"""Reporte gráfico de la tabla empresas (HU G01).

Uso:
    python scripts/reporte_empresas.py empresas_limpio.csv

Lee el CSV limpio, genera tres gráficas con matplotlib, las guarda en
reportes/ e imprime la ruta de cada una junto con las conclusiones.
"""

import os
import re
import sys

import matplotlib

# Backend sin ventana: el script nunca se queda esperando (no usa plt.show()).
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

CARPETA_SALIDA = "reportes"
DPI = 120

# Valores que se interpretan como "empresa activa" (en minúsculas).
VALORES_ACTIVA = {"true", "1", "si", "sí", "activa", "activo", "verdadero", "s", "y", "yes"}

# Patrón sencillo de correo válido: algo@dominio.ext (sin espacios ni doble @).
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def leer_datos(ruta_csv):
    """Lee el CSV limpio y devuelve un DataFrame; termina con mensaje claro si falla."""
    if not os.path.isfile(ruta_csv):
        sys.exit(f"Error: no se encontró el archivo '{ruta_csv}'.")
    try:
        df = pd.read_csv(ruta_csv)
    except Exception as error:  # archivo vacío, mal codificado, etc.
        sys.exit(f"Error: no se pudo leer '{ruta_csv}': {error}")

    # Se normalizan los nombres de columna para tolerar mayúsculas y espacios.
    df.columns = [str(c).strip().lower() for c in df.columns]
    faltantes = [c for c in ("sector", "activa") if c not in df.columns]
    if faltantes:
        sys.exit(f"Error: faltan las columnas {faltantes}. Columnas halladas: {list(df.columns)}")
    return df


def preparar_datos(df):
    """Normaliza 'sector' y 'activa' para que las gráficas cuenten bien."""
    df = df.copy()
    # Sector: sin espacios sobrantes; los vacíos quedan como 'Sin sector'.
    df["sector"] = df["sector"].fillna("").astype(str).str.strip()
    df.loc[df["sector"] == "", "sector"] = "Sin sector"
    # Activa: cualquier representación (True, 1, "sí"...) pasa a 'Activa'/'Inactiva'.
    es_activa = df["activa"].astype(str).str.strip().str.lower().isin(VALORES_ACTIVA)
    df["activa"] = es_activa.map({True: "Activa", False: "Inactiva"})
    return df


def contar_correos_invalidos(df):
    """Cuenta los correos que no cumplen el formato básico (vacíos incluidos)."""
    columna = next((c for c in ("correo", "email", "correo_electronico") if c in df.columns), None)
    if columna is None:
        return None  # el CSV no trae columna de correo
    correos = df[columna].fillna("").astype(str).str.strip()
    return int((~correos.apply(lambda c: bool(PATRON_CORREO.match(c)))).sum())


def guardar_grafica(numero):
    """Aplica tight_layout, guarda la figura actual con dpi=120, la cierra y devuelve la ruta."""
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    ruta = os.path.join(CARPETA_SALIDA, f"empresas_grafica_{numero}.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=DPI)
    plt.close()
    return ruta


def grafica_1_por_sector(df):
    """Gráfica 1 — barras: cantidad de empresas por sector."""
    por_sector = df["sector"].value_counts()
    plt.figure(figsize=(9, 6))
    por_sector.plot(kind="bar", color="#4C72B0")
    plt.title("Cantidad de empresas por sector")
    plt.xlabel("Sector")
    plt.ylabel("Número de empresas")
    plt.xticks(rotation=30, ha="right")
    return guardar_grafica(1)


def grafica_2_activas_inactivas(df):
    """Gráfica 2 — torta: empresas activas vs inactivas."""
    plt.figure(figsize=(6, 6))
    # reindex fija el orden Activa/Inactiva para que cada color corresponda a su estado
    conteo = df["activa"].value_counts().reindex(["Activa", "Inactiva"], fill_value=0)
    conteo.plot(kind="pie", autopct="%1.1f%%", colors=["#55A868", "#C44E52"])
    plt.title("Empresas activas vs inactivas")
    plt.xlabel("Estado de la empresa")
    plt.ylabel("Número de empresas")
    return guardar_grafica(2)


def grafica_3_apiladas(df):
    """Gráfica 3 — barras apiladas: activas e inactivas por sector."""
    tabla = pd.crosstab(df["sector"], df["activa"])
    for estado in ("Activa", "Inactiva"):  # garantiza ambas columnas aunque falte una
        if estado not in tabla.columns:
            tabla[estado] = 0
    tabla = tabla[["Activa", "Inactiva"]]
    plt.figure(figsize=(9, 6))
    tabla.plot(kind="bar", stacked=True, color=["#55A868", "#C44E52"], ax=plt.gca())
    plt.title("Empresas activas e inactivas por sector")
    plt.xlabel("Sector")
    plt.ylabel("Número de empresas")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Estado")
    return guardar_grafica(3)


def imprimir_conclusiones(df, correos_invalidos):
    """Imprime las conclusiones: sector líder, % inactivas y correos inválidos."""
    total = len(df)
    por_sector = df["sector"].value_counts()
    maximo = por_sector.iloc[0]
    lideres = list(por_sector[por_sector == maximo].index)
    inactivas = int((df["activa"] == "Inactiva").sum())
    pct_inactivas = inactivas / total * 100

    print("\nCONCLUSIONES")
    print("-" * 60)
    if len(lideres) == 1:
        print(f"1. El sector con más empresas registradas es '{lideres[0]}' "
              f"({maximo} de {total}, {maximo / total * 100:.1f}%).")
    else:
        print(f"1. Hay empate en el sector con más empresas: {', '.join(lideres)} "
              f"({maximo} empresas cada uno).")

    print(f"2. El {pct_inactivas:.1f}% de las empresas está inactivo ({inactivas} de {total}). "
          "Para la plataforma significa que ese porcentaje de empresas registradas no está "
          "operando: infla las cifras de usuarios, no genera actividad y conviene "
          "contactarlas para reactivarlas o depurar la base.")

    if correos_invalidos is None:
        print("3. El archivo no trae columna de correo, así que no se pudieron contar "
              "correos inválidos.")
    else:
        print(f"3. Aparecieron {correos_invalidos} correos inválidos. Hay que validarlos en el "
              "back porque la limpieza o la validación del front se puede saltar (llamadas "
              "directas a la API, datos importados), y un correo malo rompe notificaciones, "
              "recuperación de contraseña y la unicidad de las cuentas.")


def main():
    """Punto de entrada: lee el CSV, crea las tres gráficas e imprime resultados."""
    if len(sys.argv) != 2:
        sys.exit("Uso: python scripts/reporte_empresas.py empresas_limpio.csv")

    df = preparar_datos(leer_datos(sys.argv[1]))
    if df.empty:
        sys.exit("Error: el archivo no tiene filas para graficar.")
    correos_invalidos = contar_correos_invalidos(df)

    print("Gráficas generadas:")
    for ruta in (grafica_1_por_sector(df), grafica_2_activas_inactivas(df), grafica_3_apiladas(df)):
        print(f"  - {ruta}")

    imprimir_conclusiones(df, correos_invalidos)


if __name__ == "__main__":
    main()