import re
import pandas as pd
import unicodedata

def normalizar_palabra(palabra):  # con clave y valor . metemos la normalizacion de palabras
    equivalencias = {
        "automatico": "automatica",
        "automatica": "automatica",

        "manual": "manual",

        "naftero": "nafta",
        "naftera": "nafta",
        "gasolero": "diesel",
        "gasolera": "diesel",
    }

    return equivalencias.get(palabra, palabra)

def normalizar_texto(texto):
    texto = str(texto).lower().strip()
    
    texto= unicodedata.normalize("NFD",texto)
    texto= texto.encode("ascii" , "ignore").decode("utf-8") # El utf es para trabajar con las tildes del texto 
    
    return texto
def limpiar_signos(texto):
    return re.sub(r"[^a-z0-9\s]", " ", texto)

def extraer_anio(texto):
    coincidencia = re.search(r"\b(19|20)\d{2}\b", texto)

    if coincidencia:
        return int(coincidencia.group())

    return None


def limpiar_precio(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    valor = valor.replace("$", "").replace(" ", "")

    # Si viene con decimales tipo 12.600.000,00
    # cortamos antes de la coma
    if "," in valor:
        valor = valor.split(",")[0]

    valor = valor.replace(".", "")

    try:
        return int(valor)
    except ValueError:
        return None

def extraer_precio_minimo(texto): # filtro de desde 
    texto = normalizar_texto(texto)

    if "desde" not in texto and "a partir de" not in texto:
        return None

    numeros = re.findall(r"\d+", texto)

    if not numeros:
        return None

    numero = int(numeros[0])

    if "millon" in texto or "millones" in texto:
        numero *= 1_000_000 # lleva un numero de 20 a millones 

    return numero

def extraer_precio_maximo(texto):
    texto = normalizar_texto(texto)

    numeros = re.findall(r"\d+", texto)

    if not numeros:
        return None

    if "hasta" in texto:
        numero=int(numeros[-1])
    elif "menos de" in texto:
        numero=int(numeros[0])
    elif "tengo" in texto or "cuento con" in texto or "presupuesto" in texto:
        numero = int(numeros[0])
    else:
        return None
    
    if "millon" in texto or "millones" in texto:
        numero * 1_000_000

    return numero
def es_consulta_presupuesto(texto):
    texto = normalizar_texto(texto)

    palabras = [
        "tengo",
        "cuento con",
        "dispongo de",
        "presupuesto",
        "mi presupuesto",
        "hasta",
        "menos de"
    ]

    return any(palabra in texto for palabra in palabras)

def pide_economico(texto):
    palabras = [
        "economico",
        "barato",
        "barata",
        "accesible",
        "bajo precio",
        "menor precio"
    ]

    return any(palabra in texto for palabra in palabras)

def filtrar_autos(df, texto):
    texto = normalizar_texto(texto)
    resultado = df.copy()
   
    anio = extraer_anio(texto)
    precio_maximo = extraer_precio_maximo(texto)
    precio_minimo = extraer_precio_minimo(texto)
    # FILTRO POR AÑO
     # FILTRO POR AÑO
    if anio and "año" in resultado.columns:
        resultado["anio_num"] = pd.to_numeric(resultado["año"], errors="coerce")

        resultado = resultado[
            resultado["anio_num"] == anio
    ]

    # FILTRO POR PRECIO MÁXIMO
    if precio_maximo and "precio_lista" in resultado.columns:
        resultado["precio_num"] = resultado["precio_lista"].apply(limpiar_precio)
        resultado = resultado[
            resultado["precio_num"].notna() &
            (resultado["precio_num"] <= precio_maximo)
        ]
    if precio_minimo and "precio_lista" in resultado.columns:
        resultado["precio_num"] = resultado["precio_lista"].apply(limpiar_precio)
        resultado = resultado[
        resultado["precio_num"].notna() &
        (resultado["precio_num"] >= precio_minimo)
    ]
    
    if pide_economico(texto) and "precio_lista" in resultado.columns:
        resultado["precio_num"] = resultado["precio_lista"].apply(limpiar_precio)
        resultado = resultado[
        resultado["precio_num"].notna()
    ].sort_values("precio_num", ascending=True)
        
    # Sacar números del texto para no buscar "2022" dos veces
    texto_sin_numeros = re.sub(r"\b(19|20)\d{2}\b", "", texto)
    texto_sin_numeros = re.sub(r"\d+", "", texto_sin_numeros)
    texto_sin_numeros = limpiar_signos(texto_sin_numeros).strip()

    palabras = texto_sin_numeros.split()

    palabras_ignoradas = [ #Donde van esas palabras entre lineas para disparar el filtro
    "tenes",
    "tienes",
    "tienen",
    "hay",
    "busco",
    "quiero",
    "necesito",
    "me",
    "interesa",
    "interesan",
    "un",
    "una",
    "unos",
    "unas",
    "el",
    "la",
    "los",
    "las",
    "de",
    "del",
    "que",
    "con",
    "para",
    "por",
    "auto",
    "autos",
    "autito",
    "vehiculo",
    "vehiculos",
    "carro",
    "carrito",
    "modelo",
    "modelos",
    "desde",
    "algo",
    "alguno",
    "alguna",
    "opcion",
    "opción",
    "opciones",
    "teniendo",
    "algun",
    "alguna",
    "algunos",
    "algunas",
    "algo",
    "ano",
    "año",
    "anios",
    "años",
    "valor",
    "vale",
    "valga",
    "cueste",
    "cuesta",
    "tiene",
    "tenes",
    "tenés",
    
    #palabras comerciales de precio
    "economico",
    "economica",
    "barato",
    "barata",
    "accesible",
    "bajo",
    "precio",
    "menor",
    
    # verbos comunes de usuario
    "ver",
    "mostrar",
    "mostrame",
    "mostrarme",
    "muéstrame",
    "muestrame",
    "pasame",
    "pasar",
    "ofrecer",
    "ofreces",

    # precio
    "hasta",
    "desde",
    "menos",
    "mas",
    "más",
    "millones",
    "millon",
    "economico",
    "economica",
    "economicos",
    "economicas",
    "barato",
    "barata",
    "baratos",
    "baratas",
    "accesible",
    "bajo",
    "precio",
    "menor",
    "valor",
    "vale",
    "valga",
    "cueste",
    "cuesta",
    
    # transmisión
    "caja",
    "transmision",
    "transmisiones",
    "cambio",
    "cambios"
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
        normalizar_palabra(palabra)
        for palabra in palabras
        if palabra not in palabras_ignoradas
    ]
    if not palabras_utiles:
        return resultado
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

