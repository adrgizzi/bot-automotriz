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
        "tenes", "tenés", "tienen", "hay", "busco", "quiero", "necesito" , "interesa"
        "auto", "vehiculo", "vehículo", "modelo"
    ]

    return any(palabra in texto for palabra in palabras)