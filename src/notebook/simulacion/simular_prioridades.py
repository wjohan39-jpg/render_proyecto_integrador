import random
import uuid

import pandas as pd
from faker import Faker

# 1. Pais y lenguaje para simular los datos
fake = Faker("es_CO")

# 2. Semillas fijas (para que el archivo sea reproducible)
Faker.seed(42)
random.seed(42)

# 3. Constantes
FILAS = 200
NIVELES = {"Baja": 1, "Media": 2, "Alta": 3}   # nombre -> nivel
DIAS = {1: 12, 2: 7, 3: 4}                      # nivel -> dias_max_respuesta
PALABRAS_NIVEL = {1: "uno", 2: "dos", 3: "tres"}


# 4. Generar datos limpios
def _generar_filas(n):
    filas = []
    for _ in range(n):
        nombre = random.choice(list(NIVELES.keys()))
        nivel = NIVELES[nombre]
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "nivel": nivel,
            "dias_max_respuesta": DIAS[nivel],
        })
    return filas


# 5. Ensuciar datos
def _muestra(df, porcentaje):
    return df.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index


def _ensuciar(df):
    df = df.copy()
    # columnas que van a mezclar tipos (texto, None, numeros)
    df["nivel"] = df["nivel"].astype(object)
    df["dias_max_respuesta"] = df["dias_max_respuesta"].astype(object)

    # nombre: 'ALTA', ' alta ', 'Alta'
    def escribir_mal(texto):
        return random.choice([texto.upper(), f" {texto.lower()} ", texto.capitalize()])

    idx = _muestra(df, 0.10)
    df.loc[idx, "nombre"] = df.loc[idx, "nombre"].map(escribir_mal)

    # nivel: a veces texto ('3'), a veces la palabra ('tres')
    def nivel_mal(valor):
        return random.choice([str(valor), PALABRAS_NIVEL[valor]])

    idx = _muestra(df, 0.14)
    df.loc[idx, "nivel"] = df.loc[idx, "nivel"].map(nivel_mal)

    # nivel: 7% en None
    idx = _muestra(df, 0.07)
    df.loc[idx, "nivel"] = None

    # dias_max_respuesta: 5% en None
    idx = _muestra(df, 0.05)
    df.loc[idx, "dias_max_respuesta"] = None

    # dias_max_respuesta: 3% con valor absurdo (999)
    idx = _muestra(df, 0.03)
    df.loc[idx, "dias_max_respuesta"] = 999

    # 8% de filas repetidas tal cual (duplicados exactos)
    repetidas = df.loc[_muestra(df, 0.08)]
    df = pd.concat([df, repetidas], ignore_index=True)
    return df


# 6. Funcion principal (la importa exportar_prioridades.py)
def generar_prioridades(n=FILAS):
    df = pd.DataFrame(_generar_filas(n))
    df = _ensuciar(df)
    return df


if __name__ == "__main__":
    df = generar_prioridades()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())