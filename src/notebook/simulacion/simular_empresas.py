import random
import uuid
from faker import Faker
import pandas as pd

# 1-Escoger el pais y lenguaje para simular los datos
fake = Faker('es_CO')

# 2-Sembrar semillas
Faker.seed(42)
random.seed(42)

# 3-Constantes
FILAS = 300
SECTORES = ["Tecnologia", "Salud", "Manufactura", "Energia"]


# 4-Generador de datos limpios
def generar_empresas_limpias(n=FILAS):
    filas = []
    for _ in range(n):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.company(),
            "nit": fake.numerify("#########-#"),
            "sector": random.choice(SECTORES),
            "contacto": fake.name(),
            "correo": fake.company_email(),
            "telefono": fake.numerify("3#########"),
            "activa": random.choice([True, False]),
        })
    return pd.DataFrame(filas)


def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index


# 5-Ensuciar los datos
def ensuciar_datos(datos_df, porcentaje_duplicados=0.05):
    datos_df = datos_df.copy()

    # nombre: 10% con espacios sobrantes; 15% en MAYUSCULAS
    s_espacios = generar_muestra(datos_df, 0.10)
    s_mayus = generar_muestra(datos_df, 0.15)
    datos_df.loc[s_espacios, "nombre"] = datos_df.loc[s_espacios, "nombre"].apply(lambda x: f" {x} ")
    datos_df.loc[s_mayus, "nombre"] = datos_df.loc[s_mayus, "nombre"].apply(lambda x: x.upper())

    # nit: la mitad sin puntos ni guion (9001234567), la otra mitad con ellos (900.123.456-7)
    s_nit = generar_muestra(datos_df, 0.50)
    resto = ~datos_df.index.isin(s_nit)
    datos_df.loc[s_nit, "nit"] = datos_df.loc[s_nit, "nit"].apply(lambda x: x.replace("-", "").replace(".", ""))
    datos_df.loc[resto, "nit"] = datos_df.loc[resto, "nit"].apply(
        lambda x: x.replace("-", "")
    ).apply(lambda x: f"{x[:3]}.{x[3:6]}.{x[6:9]}-{x[9:]}")

    # sector: variantes 'Tecnologia', 'TECNOLOGIA', ' tecnologia '
    s_sec_mayus = generar_muestra(datos_df, 0.10)
    s_sec_esp = generar_muestra(datos_df, 0.10)
    datos_df.loc[s_sec_mayus, "sector"] = datos_df.loc[s_sec_mayus, "sector"].apply(lambda x: x.upper())
    datos_df.loc[s_sec_esp, "sector"] = datos_df.loc[s_sec_esp, "sector"].apply(lambda x: f" {x.strip().lower()} ")

    # contacto: 8% en None
    s_contacto = generar_muestra(datos_df, 0.08)
    datos_df.loc[s_contacto, "contacto"] = None

    # correo: 6% sin la arroba
    s_correo = generar_muestra(datos_df, 0.06)
    datos_df.loc[s_correo, "correo"] = datos_df.loc[s_correo, "correo"].apply(lambda x: x.replace("@", ""))

    # telefono: tres formatos mezclados (un tercio cada uno)
    s_tel1 = generar_muestra(datos_df, 0.33)
    datos_df.loc[s_tel1, "telefono"] = datos_df.loc[s_tel1, "telefono"].apply(
        lambda x: f"{x[:3]} {x[3:6]} {x[6:]}")
    s_tel2 = generar_muestra(datos_df.drop(s_tel1), 0.50)
    datos_df.loc[s_tel2, "telefono"] = datos_df.loc[s_tel2, "telefono"].apply(
        lambda x: f"+57 {x[:3]}-{x[3:6]}-{x[6:]}")

    # activa: la mitad como texto 'SI', 'No', '1', '0'
    s_activa = generar_muestra(datos_df, 0.50)
    datos_df["activa"] = datos_df["activa"].astype(object)  # pandas 3 no deja guardar texto en columna booleana
    datos_df.loc[s_activa, "activa"] = datos_df.loc[s_activa, "activa"].apply(
        lambda x: random.choice(["SI" if x else "No", "1" if x else "0"]))

    # 3% de los nit repetidos entre empresas distintas (se hace ANTES de los duplicados
    # exactos para no romper la copia exacta de las filas repetidas)
    s_nit_rep = generar_muestra(datos_df, 0.03)
    nits_otras = datos_df.drop(s_nit_rep)["nit"].sample(
        n=len(s_nit_rep), random_state=random.randint(0, 9999)).values
    datos_df.loc[s_nit_rep, "nit"] = nits_otras

    # 5% de las filas repetidas tal cual (duplicados exactos), al final
    s_dup = datos_df.sample(n=round(len(datos_df) * porcentaje_duplicados / (1 - porcentaje_duplicados)),
                            random_state=random.randint(0, 9999)).index
    datos_df = pd.concat([datos_df, datos_df.loc[s_dup]], ignore_index=True)

    return datos_df


# 6-Todo se arma aqui: devuelve exactamente n filas (n-5% unicas + 5% duplicadas)
def generar_empresas(n=300):
    n_duplicadas = round(n * 0.05)
    df = generar_empresas_limpias(n - n_duplicadas)
    df = ensuciar_datos(df)
    return df


if __name__ == "__main__":
    df = generar_empresas()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())