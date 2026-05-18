import pandas as pd


SHEET_URL = "https://docs.google.com/spreadsheets/d/1fEmcM4fzV2TwmzyZVqF9yS2mxH305CarUKURpC4t1xo/export?format=csv"

def buscar_autos(query):
    df = pd.read_csv(SHEET_URL)
    
    # Eliminar filas donde marca está vacía
    df = df.dropna(subset=['marca'])
    
    df = df.rename(columns={
        'transmision': 'transmisión'
    })
    
    mascara = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    return df[mascara]


