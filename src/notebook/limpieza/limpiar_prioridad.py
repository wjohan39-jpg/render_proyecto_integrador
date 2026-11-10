"""Limpia la tabla `prioridades` del proyecto integrador (HU L01 de Kaizen).

Uso (desde la raiz del proyecto, sin argumentos):
    python main.py
o directamente:
    python src/notebook/limpieza/limpiar_prioridad.py [ruta_sucio] [carpeta_salida]

Por defecto lee `data/crudo/prioridades_sucio.csv`. Lee el CSV sucio, imprime el diagnostico, corrige los errores que piden los
criterios, imprime el diagnostico otra vez y guarda en `carpeta_salida`
(por defecto `data/limpio/`):
    - prioridades_limpio.csv
    - prioridades_catalogo.csv
"""
import os
import sys

import pandas as pd

# Columnas que no pueden quedar con nulos despues de limpiar
COLUMNAS_OBLIGATORIAS = ["id", "nombre", "nivel", "dias_max_respuesta"]

# Columnas sin las que el script no puede limpiar
COLUMNAS_NECESARIAS = ["nombre", "nivel", "dias_max_respuesta"]

# Catalogo base nombre -> nivel (se completa con lo que traigan los datos)
NIVELES_BASE = {"Baja": 1, "Media": 2, "Alta": 3}

# Niveles escritos en palabra -> numero
NIVEL_EN_PALABRA = {"tres": 3, "dos": 2, "uno": 1, "cuatro": 4, "cinco": 5}

# Dias por encima de este valor se consideran absurdos
DIAS_MAXIMOS_VALIDOS = 60

RUTA_SUCIO_POR_DEFECTO = os.path.join("data", "crudo", "prioridades_sucio.csv")
CARPETA_SALIDA_POR_DEFECTO = os.path.join("data", "limpio")


def columnas_obligatorias(df):
    """Devuelve las columnas obligatorias que existen en el DataFrame (no exige 'id' si el CSV no la trae)."""
    return [c for c in COLUMNAS_OBLIGATORIAS if c in df.columns]


def imprimir_titulo(texto):
    """Imprime un titulo visible para separar las secciones de la salida."""
    print(f"\n{'*' * 10} {texto} {'*' * 10}")


def diagnostico_inicial(df):
    """Muestra el tamaño, la info, los nulos y los duplicados exactos del DataFrame sucio."""
    imprimir_titulo("DIAGNOSTICO INICIAL")
    print("Tamaño (filas, columnas):", df.shape)
    df.info()
    print("\nNulos por columna:")
    print(df.isna().sum())
    print("\nDuplicados exactos:", df.duplicated().sum())


def diagnostico_final(df, filas_iniciales):
    """Muestra el tamaño y los nulos del DataFrame limpio y cuantas filas se eliminaron."""
    imprimir_titulo("DIAGNOSTICO FINAL")
    print("Tamaño (filas, columnas):", df.shape)
    print("\nNulos por columna:")
    print(df.isna().sum())
    print("\nDuplicados exactos:", df.duplicated().sum())
    print("Filas eliminadas:", filas_iniciales - len(df))


def unificar_nombre(df):
    """Quita espacios y deja solo la primera letra en mayuscula (' ALTA ' -> 'Alta')."""
    df["nombre"] = df["nombre"].str.strip().str.capitalize()
    # Un nombre vacio ('') se trata como nulo
    df["nombre"] = df["nombre"].replace("", None)
    return df


def convertir_nivel(df):
    """Convierte 'tres', 'dos', 'uno' y '3' a numero; lo que no se pueda queda como nulo."""
    # Se pasa a object y se normaliza el texto para que el replace funcione en pandas 2 y 3
    nivel = df["nivel"].astype(object)
    nivel = nivel.map(lambda valor: valor.strip().lower() if isinstance(valor, str) else valor)
    df["nivel"] = nivel.replace(NIVEL_EN_PALABRA)
    df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce")
    return df


def construir_niveles(df):
    """Arma el diccionario nombre -> nivel con el catalogo base y el nivel mas comun de cada nombre."""
    niveles = dict(NIVELES_BASE)
    conocidos = df.dropna(subset=["nombre", "nivel"])
    for nombre, grupo in conocidos.groupby("nombre"):
        niveles.setdefault(nombre, grupo["nivel"].mode().iloc[0])
    return niveles


def rellenar_nivel(df, niveles):
    """Rellena el nivel vacio usando el nombre de la prioridad."""
    df["nivel"] = df["nivel"].fillna(df["nombre"].map(niveles))
    return df


def limpiar_dias(df):
    """Convierte los dias a numero, marca como nulo lo absurdo (> 60) y rellena con la mediana.

    Devuelve el DataFrame y una mascara con las filas cuyo valor fue imputado.
    """
    df["dias_max_respuesta"] = pd.to_numeric(df["dias_max_respuesta"], errors="coerce")
    df.loc[df["dias_max_respuesta"] > DIAS_MAXIMOS_VALIDOS, "dias_max_respuesta"] = None
    imputados = df["dias_max_respuesta"].isna()
    mediana = df["dias_max_respuesta"].median()
    print(f"Dias imputados con la mediana ({mediana}):", int(imputados.sum()))
    df["dias_max_respuesta"] = df["dias_max_respuesta"].fillna(mediana)
    return df, imputados


def sacar_catalogo(df, imputados):
    """Saca una fila por nombre (catalogo real), prefiriendo filas con dias originales sobre imputados."""
    catalogo = (
        df.assign(_imputado=imputados)
        .sort_values("_imputado", kind="stable")
        .drop_duplicates(subset=["nombre"])
        .drop(columns=["id", "_imputado"], errors="ignore")
        .sort_values("nivel")
        .reset_index(drop=True)
    )
    return catalogo


def verificar(df):
    """Comprueba que no queden nulos en columnas obligatorias ni duplicados exactos."""
    nulos = int(df[columnas_obligatorias(df)].isna().sum().sum())
    duplicados = int(df.duplicated().sum())
    imprimir_titulo("VERIFICACION")
    print("Nulos en columnas obligatorias:", nulos)
    print("Duplicados exactos:", duplicados)
    return nulos == 0 and duplicados == 0


def limpiar(df):
    """Aplica todos los pasos de limpieza de la HU L01 y devuelve (limpio, catalogo)."""
    imprimir_titulo("LIMPIEZA")
    df = df.drop_duplicates().copy()
    df = unificar_nombre(df)
    df = convertir_nivel(df)
    df = rellenar_nivel(df, construir_niveles(df))
    df, imputados = limpiar_dias(df)

    # Filas que no se pueden recuperar (sin id o sin nombre) se eliminan
    recuperables = df[columnas_obligatorias(df)].notna().all(axis=1)
    if (~recuperables).any():
        print("Filas sin datos obligatorios recuperables (se eliminan):", int((~recuperables).sum()))
    df, imputados = df[recuperables].copy(), imputados[recuperables]

    # Nivel y dias vuelven a ser enteros
    df["nivel"] = df["nivel"].astype(int)
    df["dias_max_respuesta"] = df["dias_max_respuesta"].astype(int)

    # Al unificar textos pueden aparecer duplicados nuevos
    sin_duplicar = ~df.duplicated()
    df, imputados = df[sin_duplicar], imputados[sin_duplicar]

    catalogo = sacar_catalogo(df, imputados)
    return df, catalogo


def guardar(df, catalogo, carpeta_salida):
    """Crea la carpeta de salida si no existe y guarda el limpio y el catalogo en CSV."""
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta_limpio = os.path.join(carpeta_salida, "prioridades_limpio.csv")
    ruta_catalogo = os.path.join(carpeta_salida, "prioridades_catalogo.csv")
    df.to_csv(ruta_limpio, index=False, encoding="utf-8")
    catalogo.to_csv(ruta_catalogo, index=False, encoding="utf-8")
    return ruta_limpio, ruta_catalogo


def main():
    """Lee los argumentos, ejecuta el diagnostico, la limpieza y guarda los archivos."""
    ruta_sucio = sys.argv[1] if len(sys.argv) > 1 else RUTA_SUCIO_POR_DEFECTO
    carpeta_salida = sys.argv[2] if len(sys.argv) > 2 else CARPETA_SALIDA_POR_DEFECTO
    if not os.path.isfile(ruta_sucio):
        print(f"No existe el archivo: {ruta_sucio}")
        sys.exit(1)

    df = pd.read_csv(ruta_sucio)
    faltan = [c for c in COLUMNAS_NECESARIAS if c not in df.columns]
    if faltan:
        print(f"Al archivo le faltan columnas: {faltan}. Columnas encontradas: {list(df.columns)}")
        sys.exit(1)
    filas_iniciales = len(df)

    diagnostico_inicial(df)
    df, catalogo = limpiar(df)
    diagnostico_final(df, filas_iniciales)

    imprimir_titulo("CATALOGO REAL")
    print(catalogo.to_string(index=False))
    print(f"Filas del catalogo: {len(catalogo)} (los criterios esperan 5)")

    correcto = verificar(df)
    ruta_limpio, ruta_catalogo = guardar(df, catalogo, carpeta_salida)
    imprimir_titulo("ARCHIVOS GENERADOS")
    print(f"{ruta_limpio} | tamaño: {df.shape}")
    print(f"{ruta_catalogo} | tamaño: {catalogo.shape}")

    if not correcto:
        print("\nATENCION: quedan nulos o duplicados; revisa los datos de entrada.")
        sys.exit(1)


if __name__ == "__main__":
    main()