import random
import uuid
from datetime import timedelta

import pandas as pd
from faker import Faker

# 1. Escoger el país y el lenguaje para simular los datos
fake = Faker("es_CO")

# 2. Sembrar semillas (para que el archivo sea reproducible)
Faker.seed(42)
random.seed(42)

# 3. Constantes (listas fijas para que varios retos compartan empresa, categoría y prioridad)
FILAS = 500

ESTADOS = ["pendiente", "en progreso", "completada"]
IDS_EMPRESA = [
    "c8f9b7d4-3a2e-4c1f-9b6d-7e5f4a3b2c1d",
    "d9a0c8e5-4b3f-4d20-a7c1-8f6e5b4a3d2c",
    "e0b1d9f6-5c4a-4e31-b8d2-9a7f6c5b4e3d",
    "f1c2e0a7-6d5b-4f42-c9e3-a8b7d6c5f4e0",
    "a2d3f1b8-7e6c-4053-da4f-b9c8e7d6a5f1",
]
IDS_CATEGORIA = [
    "b3e4a2c9-8f7d-4164-eb5a-c0d9f8e7b6a2",
    "c4f5b3d0-9a8e-4275-fc6b-d1e0a9f8c7b3",
    "d5a6c4e1-0b9f-4386-ad7c-e2f1b0a9d8c4",
    "e6b7d5f2-1c0a-4497-be8d-f3a2c1b0e9d5",
]
IDS_PRIORIDAD = [
    "f7c8e6a3-2d1b-45a8-cf9e-a4b3d2c1f0e6",
    "a8d9f7b4-3e2c-46b9-d0af-b5c4e3d2a1f7",
    "b9e0a8c5-4f3d-47ca-e1b0-c6d5f4a3b2e8",
]


# 4. Generar los datos limpios
def generar_retos(n=FILAS):
    """Genera n retos simulados, los ensucia y devuelve el DataFrame."""
    filas = []
    for _ in range(n):
        fecha_inicio = fake.date_between(start_date="-1y", end_date="+3m")
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(nb_words=6).rstrip("."),
            "descripcion": fake.sentence(nb_words=12),
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_inicio + timedelta(days=random.randint(15, 180)),
            "estado": random.choice(ESTADOS),
            "id_empresa": random.choice(IDS_EMPRESA),
            "id_categoria": random.choice(IDS_CATEGORIA),
            "id_prioridad": random.choice(IDS_PRIORIDAD),
        })

    # El DataFrame se arma y se ensucia DESPUÉS del ciclo
    df = pd.DataFrame(filas)
    df = ensuciar(df)
    return df


# 5. Ensuciar los datos
def generar_muestra(datos, porcentaje, total=None):
    """Devuelve el índice de una muestra de filas.
    El tamaño es porcentaje * total (por defecto, el tamaño de datos)."""
    total = len(datos) if total is None else total
    cantidad = round(porcentaje * total)
    return datos.sample(n=cantidad, random_state=random.randint(0, 9999)).index


def ensuciar(datos_df):
    """Aplica los errores pedidos por la HU y devuelve un DataFrame nuevo."""
    datos_df = datos_df.copy()
    total = len(datos_df)

    # nombre: 10% con espacios sobrantes
    idx = generar_muestra(datos_df, 0.10)
    datos_df.loc[idx, "nombre"] = " " + datos_df.loc[idx, "nombre"] + " "

    # descripcion: 12% en None
    idx = generar_muestra(datos_df, 0.12)
    datos_df.loc[idx, "descripcion"] = None

    # Se pasan las fechas a datetime para poder operarlas
    inicio = pd.to_datetime(datos_df["fecha_inicio"])
    fin = pd.to_datetime(datos_df["fecha_fin"])

    # fecha_fin: 5% ANTERIOR a fecha_inicio (error lógico), de 1 a 30 días antes
    idx_error = generar_muestra(datos_df, 0.05)
    dias = pd.to_timedelta([random.randint(1, 30) for _ in idx_error], unit="D")
    fin.loc[idx_error] = inicio.loc[idx_error] - dias

    # fecha_fin: 8% en None (en filas distintas a las del error lógico)
    idx_nulos = generar_muestra(datos_df.drop(index=idx_error), 0.08, total)
    fin.loc[idx_nulos] = pd.NaT

    datos_df["fecha_fin"] = fin.dt.strftime("%Y-%m-%d").astype(object).where(fin.notna(), None)

    # fecha_inicio: dos formatos mezclados (2026-03-02 y 02/03/2026), 40% en formato latino
    iso = inicio.dt.strftime("%Y-%m-%d")
    latino = inicio.dt.strftime("%d/%m/%Y")
    datos_df["fecha_inicio"] = iso
    idx = generar_muestra(datos_df, 0.40)
    datos_df.loc[idx, "fecha_inicio"] = latino.loc[idx]

    # estado: 14% con variantes mal escritas
    def escribir_mal(_texto):
        return random.choice(["en_curso", "EN CURSO", " Cerrado "])

    idx = generar_muestra(datos_df, 0.14)
    datos_df.loc[idx, "estado"] = datos_df.loc[idx, "estado"].apply(escribir_mal)

    # 5% de filas repetidas tal cual (duplicados exactos)
    idx = generar_muestra(datos_df, 0.05)
    datos_df = pd.concat([datos_df, datos_df.loc[idx]], ignore_index=True)

    return datos_df


if __name__ == "__main__":
    df = generar_retos()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())