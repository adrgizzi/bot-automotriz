def es_financiacion(texto):
    return "financi" in texto or "cuota" in texto or "credito" in texto or "crédito" in texto


def es_permuta(texto):
    return "permuta" in texto or "entrego" in texto or "parte de pago" in texto


def es_fotos(texto):
    return "foto" in texto or "fotos" in texto or "imagen" in texto


def es_saludo(texto):
    return "hola" in texto or "buenas" in texto

def parece_busqueda_auto(texto):
    palabras = [
        "tenes",
        "tenés",
        "tienes",
        "tienen",
        "hay",
        "busco",
        "quiero",
        "necesito",
        "me interesa",
        "mostrar",
        "mostrame",
        "mostrarme",
        "muestrame",
        "ver",
        "pasame",
        "auto",
        "autos",
        "vehiculo",
        "vehículo",
        "vehiculos",
        "modelo",
        "marca",
        "barato",
        "economico",
        "económico",
        "hasta",
        "desde",
        "algo",
        "algun",
        "quiero ver"
        
    ]

    return any(palabra in texto for palabra in palabras)


def es_asesor(texto):
    palabras = [
        "asesor",
        "vendedor",
        "persona",
        "humano",
        "contactar",
        "contacto",
        "whatsapp",
        "llamar",
        "hablar"
    ]

    return any(palabra in texto for palabra in palabras)

def es_compra(texto):
    palabras = [
        "quiero comprar",
        "comprar",
        "me interesa comprar",
        "quiero avanzar",
        "quiero señar",
        "señar",
        "reservar",
        "lo quiero",
        "me lo llevo",
        "quiero verlo",
        "quiero coordinar",
        "cerrar",
        "avanzar",
        "quiero llevarme",
        "ese mismo",
        "me llevo",
        "esa misma",
        "la quiero",
        "esa"
    ]

    return any(palabra in texto for palabra in palabras)


#desde aca procesamos todas las palabras raras dentro del sistema lo que sea que no este del todo bien esto lo puede tomar como una intencion de respuesta o de "compra". la idea es siempre mantener el dialogo 

