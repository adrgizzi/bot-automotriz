import pandas as pd
import time # Para el cache 
from app.services.filters import filtrar_autos #filtro de auto
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fEmcM4fzV2TwmzyZVqF9yS2mxH305CarUKURpC4t1xo/export?format=csv"

_cache_df = None # aca se guarda la planilla
_cache_time = 0 # aca se guarda cuando se descargo por ultima vez
CACHE_SECONDS = 300  # 5 minutos de cache antes de volver a leer la planilla 

def obtener_dataframe():
    global _cache_df, _cache_time

    ahora = time.time() 
 
    if _cache_df is not None and ahora - _cache_time < CACHE_SECONDS: # comprueba que esta por debajo del tiempo 
        return _cache_df.copy()

    df = pd.read_csv(SHEET_URL)  # Si venció el cache, lee la planilla otra vez
    df.columns = df.columns.str.strip().str.lower()

    _cache_df = df
    _cache_time = ahora

    return df.copy()

def buscar_autos(texto):
    texto = texto.lower().strip()

    df = obtener_dataframe()

    return filtrar_autos(df, texto)

def obtener_autos():
    return obtener_dataframe()
#Lista de prioridades :

#sheets.py = obtiene datos
#filters.py = decide qué autos coinciden
#responses.py = arma la respuesta para el cliente