import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1fEmcM4fzV2TwmzyZVqF9yS2mxH305CarUKURpC4t1xo/export?format=csv"

def buscar_autos(query):

    df = pd.read_csv(SHEET_URL)

    resultados = df[
        df["modelo"].str.lower().str.contains(query.lower(), na=False)
    ]

    return resultados