import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1fEmcM4fzV2TwmzyZVqF9yS2mxH305CarUKURpC4t1xo/export?format=csv"


def obtener_dataframe():

    df = pd.read_csv(SHEET_URL)

    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip().str.lower()

    return df


def buscar_autos(texto):

    texto = texto.lower()

    df = obtener_dataframe()
    print(df["marca"])
    print(texto)

    df["marca"] = df["marca"].astype(str).str.lower().str.strip()
    df["modelo"] = df["modelo"].astype(str).str.lower().str.strip()

    resultado = df[
        df["marca"].str.contains(texto, na=False) |
        df["modelo"].str.contains(texto, na=False)
    ]

    return resultado
