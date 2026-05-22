import re
import pandas as pd
import unicodedata


def normalizar_texto(texto):
    texto = str(texto).lower().strip()
    
    texto= unicodedata.normalize("NFD",texto)
    texto= texto.encode("ascii" , "ignore").decode("utf-8")
    
    return texto


def extraer_anio(texto):
    coincidencia = re.search(r"\b(19|20)\d{2}\b", texto)

    if coincidencia:
        return int(coincidencia.group())

    return None


def limpiar_precio(valor):
    if pd.isna(valor):
        return None

    valor = str(valor)
    valor = valor.replace("$", "")
    valor = valor.replace(".", "")
    valor = valor.replace(",", "")
    valor = valor.strip()

    try:
        return int(valor)
    except ValueError:
        return None


def extraer_precio_maximo(texto):
    texto = texto.lower()

    if "hasta" not in texto and "menos de" not in texto:
        return None

    numeros = re.findall(r"\d+", texto)

    if not numeros:
        return None

    numero = int(numeros[0])

    if "millon" in texto or "millones" in texto:
        numero *= 1_000_000

    return numero


def filtrar_autos(df, texto):
    texto = normalizar_texto(texto)
    resultado = df.copy()

    anio = extraer_anio(texto)
    precio_maximo = extraer_precio_maximo(texto)

    # FILTRO POR AÑO
    if anio and "año" in resultado.columns:
        resultado = resultado[
            resultado["año"].astype(str).str.contains(str(anio), na=False)
        ]

    # FILTRO POR PRECIO MÁXIMO
    if precio_maximo and "precio_lista" in resultado.columns:
        resultado["precio_num"] = resultado["precio_lista"].apply(limpiar_precio)
        resultado = resultado[
            resultado["precio_num"].notna() &
            (resultado["precio_num"] <= precio_maximo)
        ]

    # Sacar números del texto para no buscar "2022" dos veces
    texto_sin_numeros = re.sub(r"\b(19|20)\d{2}\b", "", texto)
    texto_sin_numeros = re.sub(r"\d+", "", texto_sin_numeros).strip()

    palabras = texto_sin_numeros.split()

    palabras_ignoradas = [
        "tenes",
        "tenés",
        "tienen",
        "tienes",
        "hay",
        "busco",
        "quiero",
        "necesito",
        "me",
        "interesa",
        "un",
        "una",
        "auto",
        "vehiculo",
        "vehículo",
        "modelo",
        "hasta",
        "menos",
        "de",
        "millones",
        "millon",
        "caja",
        "con",
        "transmision",
        "transmisiòn"
    ]

    columnas_busqueda = [
        "marca",
        "modelo",
        "transmision",
        "combustible",
        "categoria",
        "color"
    ]

    palabras_utiles = [
        palabra for palabra in palabras
        if palabra not in palabras_ignoradas
    ]

    for palabra in palabras_utiles:
        filtro_palabra = False

        for columna in columnas_busqueda:
            if columna in resultado.columns:
                columnas_normalizada=resultado[columna].astype(str).apply(normalizar_texto)
                filtro_palabra = (
                    filtro_palabra |
                    columnas_normalizada.str.contains(palabra,na=False)
                )

        resultado = resultado[filtro_palabra]

    return resultado