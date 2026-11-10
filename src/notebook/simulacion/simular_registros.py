import random
import uuid

import pandas as pd
from faker import Faker


ESTADOS = ("INSCRITO", "EN PROCESO", "FINALIZADO")
IDS_USUARIO = tuple(
    str(uuid.uuid5(uuid.NAMESPACE_URL, f"integrador-registros-usuario-{index}"))
    for index in range(1, 151)
)
IDS_RETO = tuple(
    str(uuid.uuid5(uuid.NAMESPACE_URL, f"integrador-registros-reto-{index}"))
    for index in range(1, 21)
)

Faker.seed(42)
random.seed(42)


def generar_registros(n: int = 800) -> pd.DataFrame:
    if n < 1:
        raise ValueError("La cantidad de registros debe ser mayor que cero.")

    random.seed(42)
    fake = Faker("es_ES")
    fake.seed_instance(42)

    duplicados_pareja = int(n * 0.05)
    duplicados_exactos = int(n * 0.05)
    cantidad_base = n - duplicados_pareja - duplicados_exactos
    if cantidad_base > len(IDS_USUARIO) * len(IDS_RETO):
        raise ValueError("No hay suficientes combinaciones de usuario y reto para generar datos unicos.")

    pares_base = set()
    while len(pares_base) < cantidad_base:
        pares_base.add((random.choice(IDS_USUARIO), random.choice(IDS_RETO)))
    filas = [
        _crear_fila(fake, id_usuario, id_reto)
        for id_usuario, id_reto in sorted(pares_base)
    ]

    origenes_repetidos = random.sample(range(cantidad_base), duplicados_pareja)
    for indice in origenes_repetidos:
        fila = dict(filas[indice])
        fila["id"] = str(uuid.uuid4())
        fila["fecha_registro"] = fake.date_time_between(start_date="-1y", end_date="now")
        fila["observacion"] = fake.sentence(nb_words=10)
        fila["estado"] = random.choice(ESTADOS)
        filas.append(fila)

    df = pd.DataFrame(filas)
    formatos = ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M")
    df["fecha_registro"] = df["fecha_registro"].map(
        lambda fecha: fecha.strftime(random.choice(formatos))
    )
    df["estado"] = df["estado"].map(_ensuciar_estado)

    origenes_exactos = random.sample(
        [indice for indice in range(cantidad_base) if indice not in origenes_repetidos],
        duplicados_exactos,
    )
    indices_nulos = random.sample(
        [indice for indice in range(len(df)) if indice not in origenes_exactos],
        int(n * 0.2),
    )
    df.loc[indices_nulos, "observacion"] = None
    exactos = df.iloc[origenes_exactos].copy()
    return pd.concat([df, exactos], ignore_index=True)


def _crear_fila(fake: Faker, id_usuario: str, id_reto: str) -> dict[str, object]:
    return {
        "id": str(uuid.uuid4()),
        "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
        "observacion": fake.sentence(nb_words=10),
        "estado": random.choice(ESTADOS),
        "id_usuario": id_usuario,
        "id_reto": id_reto,
    }


def _ensuciar_estado(estado: str) -> str:
    variantes = {
        "INSCRITO": ("inscrito", " INSCRITO ", "Inscrito"),
        "EN PROCESO": ("EN PROCESO", "en proceso", " En Proceso "),
        "FINALIZADO": (" Finalizado ", "finalizado", "FINALIZADO"),
    }
    return random.choice(variantes[estado])


if __name__ == "__main__":
    df = generar_registros()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())