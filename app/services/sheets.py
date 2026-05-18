import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1fEmcM4fzV2TwmzyZVqF9yS2mxH305CarUKURpC4t1xo/export?format=csv"

def buscar_autos(texto):

    df = pd.read_csv(SHEET_URL)
    print("COLUMNAS:", df.columns.tolist()) 

    #print(df.head())  # muestra las primeras filas de la planilla . debug temporal 

    texto = texto.lower()

    print("Texto recibido:", texto)

    resultados = df[
        df["marca"].str.lower().str.contains(texto, na=False) |
        df["modelo"].str.lower().str.contains(texto, na=False)
    ]

    print("Resultados encontrados:")
    print(resultados)

    return resultados

