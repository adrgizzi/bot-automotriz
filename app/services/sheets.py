import pandas as pd
import time # Para el cache 
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fEmcM4fzV2TwmzyZVqF9yS2mxH305CarUKURpC4t1xo/export?format=csv"

_cache_df = None # aca se guarda la planilla
_cache_time = 0 # aca se guarda cuando se descargo por ultima vez
CACHE_SECONDS = 300  # 5 minutos busca en la panilla 


def obtener_dataframe():
    global _cache_df, _cache_time

    ahora = time.time() 
 
    if _cache_df is not None and ahora - _cache_time < CACHE_SECONDS: # comprueba que esta por debajo del tiempo 
        return _cache_df.copy()

    df = pd.read_csv(SHEET_URL) # Llega aca al vencer el cache 
    df.columns = df.columns.str.strip().str.lower()

    _cache_df = df
    _cache_time = ahora

    return df.copy()


def buscar_autos(texto):
    texto = texto.lower().strip()

    df = obtener_dataframe()

    marca_lower = df["marca"].astype(str).str.lower().str.strip()
    modelo_lower = df["modelo"].astype(str).str.lower().str.strip()

    resultado = df[
        marca_lower.str.contains(texto, na=False) |
        modelo_lower.str.contains(texto, na=False)
    ]

    return resultado
