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
    
    # Comparar en minúsculas pero sin modificar el df original
    marca_lower = df["marca"].astype(str).str.lower().str.strip()
    modelo_lower = df["modelo"].astype(str).str.lower().str.strip()
    
    resultado = df[
        marca_lower.str.contains(texto, na=False) |
        modelo_lower.str.contains(texto, na=False)
    ]
    

    return resultado
