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

def extraer_precio_minimo(texto):
    texto = normalizar_texto(texto)

    if "desde" not in texto and "entre" not in texto and "a partir de" not in texto:
        return None

    numeros = re.findall(r"\d+", texto)

    if not numeros:
        return None

    numero = int(numeros[0])

    if "millon" in texto or "millones" in texto:
        numero *= 1_000_000

    return numero


def extraer_precio_maximo(texto):
    texto = normalizar_texto(texto)

    numeros = re.findall(r"\d+", texto)

    if not numeros:
        return None

    # Caso: "desde 14 millones a 23 millones"
    if "desde" in texto and len(numeros) >= 2:
        numero = int(numeros[-1])

    # Caso: "entre 14 y 23 millones"
    elif "entre" in texto and len(numeros) >= 2:
        numero = int(numeros[-1])

    # Caso: "hasta 23 millones"
    elif "hasta" in texto:
        numero = int(numeros[-1])

    # Caso: "menos de 23 millones"
    elif "menos de" in texto:
        numero = int(numeros[0])

    # Caso: "tengo 23 millones"
    elif "tengo" in texto or "cuento con" in texto or "presupuesto" in texto:
        numero = int(numeros[0])

    else:
        return None

    if "millon" in texto or "millones" in texto:
        numero *= 1_000_000

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
    precio_minimo = extraer_precio_minimo(texto)
    precio_maximo = extraer_precio_maximo(texto)
    # FILTRO POR AÑO
    if anio and "año" in resultado.columns:
        resultado["anio_num"] = pd.to_numeric(resultado["año"], errors="coerce")

        resultado = resultado[
            resultado["anio_num"] == anio
    ]

    # FILTRO POR PRECIO MÁXIMO
    
    if precio_minimo and "precio_lista" in resultado.columns:
        resultado["precio_num"] = resultado["precio_lista"].apply(limpiar_precio)
        resultado = resultado[
            resultado["precio_num"].notna() &
            (resultado["precio_num"] >= precio_minimo)
    ]
    if "precio_num" in resultado.columns:
        resultado = resultado.sort_values("precio_num", ascending=True)
        
    if precio_maximo and "precio_lista" in resultado.columns:
        resultado["precio_num"] = resultado["precio_lista"].apply(limpiar_precio)
        resultado = resultado[
            resultado["precio_num"].notna() &
            (resultado["precio_num"] <= precio_maximo)
    ]
    if "precio_num" in resultado.columns:
        resultado = resultado.sort_values("precio_num", ascending=True)
        
    if pide_economico(texto) and "precio_lista" in resultado.columns:
        resultado["precio_num"] = resultado["precio_lista"].apply(limpiar_precio)
        resultado = resultado[
        resultado["precio_num"].notna()
    ].sort_values("precio_num", ascending=True)
    
    colores = [
    "blanco",
    "negro",
    "gris",
    "azul",
    "rojo",
    "bordo",
    "bordeau",
    "bordeaux",
    "beige",
    "verde",
    "plata"
]

    color_detectado = None

    for color in colores:
            if color in texto:
                color_detectado = color
                break
            
    if color_detectado and "color" in resultado.columns:
        color_columna = resultado["color"].astype(str).apply(normalizar_texto)

        resultado = resultado[
            color_columna.str.contains(color_detectado, na=False)
    ]
    
    
    # Sacar números del texto para no buscar "2022" dos veces
    texto_sin_numeros = re.sub(r"\b(19|20)\d{2}\b", "", texto)
    texto_sin_numeros = re.sub(r"\d+", "", texto_sin_numeros)
    texto_sin_numeros = limpiar_signos(texto_sin_numeros).strip()

    palabras = texto_sin_numeros.split()

    palabras_ignoradas = [  # filtro donde ingresan las palabras
    "tenes",
    "tienes",
    "tienen",
    "hay",
    "busco",
    "buscando",
    "estoy",
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

#Colores segunda edicion 
    "color",
    "colores",
    "pintura",
    "blanco",
    "negro",
    "gris",
    "azul",
    "rojo",
    "bordo",
    "bordeaux",
    "beige",
    "verde",
    "plata",
    "ano",
    "anos",
    "anios",

    "algun",
    "alguna",
    "algunos",
    "algunas",
    "algo",
    "opcion",
    "opciones",

    "ver",
    "mostrar",
    "mostrame",
    "mostrarme",
    "muestrame",
    "pasame",
    "pasar",
    "ofrecer",
    "ofreces",

    "hasta",
    "desde",
    "entre",
    "menos",
    "mas",
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

