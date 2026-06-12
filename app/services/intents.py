from app.services.filters import normalizar_texto

def contiene_alguna(texto,palabras):
    texto=normalizar_texto(texto)
    return any (palabra in texto for palabra in palabras)


def es_financiacion(texto):
    
    palabras=["financiacion",
        "financiar",
        "financiado",
        "financiada",
        "cuota",
        "cuotas",
        "credito",
        "prestamo",
        "anticipo",
        "entrega",
        "plan de pago",
        "se puede pagar en cuotas",
    ]


    return contiene_alguna(texto,palabras)

def es_permuta(texto):
    
    
    palabras = [
        "permuta",
        "permuto",
        "entrego",
        "entregar mi auto",
        "parte de pago",
        "toman usado",
        "tomas usado",
        "reciben usado",
        "recibis usado",
        "mi auto como parte",
    ]
    
    return contiene_alguna(texto,palabras)

def es_fotos(texto):
    palabras = [
        "foto",
        "fotos",
        "imagen",
        "imagenes",
        "ver fotos",
        "pasame fotos",
        "mostrar fotos",
        "quiero ver fotos",
        "tenes foto",
        "tenes fotos",
        "tenes imagen",
        "tenes imagenes",
        "mandame fotos",
        "mandame imagenes",
        "me pasas fotos",
        "me pasas imagenes",
        "quiero fotos",
    ]

    return contiene_alguna(texto, palabras)

def es_saludo(texto):
    texto=normalizar_texto(texto).strip()
    saludos=[
        "hola",
        "buenas",
        "buen dia",
        "buenas tardes",
        "buenas noches",
        "que tal",
        "como estas",
    ]
    return texto in saludos or any (texto.startswith(saludo)for saludo in saludos)
    
def parece_busqueda_auto(texto):
    palabras = [
           "tenes",
           "tenes",
           "tienes",
           "tienen",
           "hay",
           "busco",
           "estoy buscando",
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
           "vehiculos",
           "camioneta",
           "camionetas",
           "modelo",
           "marca",
           "barato",
           "economico",
           "hasta",
           "desde",
           "algo",
           "algun",
           "alguno",
           "quiero ver",
           "precio",
           "automatico",
           "automatica",
           "manual",
           "nafta",
           "diesel",
           "blanco",
           "negro",
           "gris",
           "rojo",
           "azul",
           "fiat",
           "peugeot",
           "toyota",
           "ford",
           "chevrolet",
           "renault",
           "volkswagen",
           "citroen",
           "honda",
           "nissan",
           "jeep",
           "cronos",
           "208",
           "etios",
           "gol",
           "onix",
           "corolla",
           "hilux",
           "sandero",
           "kangoo",
    ]
    return contiene_alguna(texto,palabras)



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
        "llamame",
        "hablar",
        "hablar con alguien",
        "quiero hablar",
        "que me contacten",
        "pasame con alguien",
    ]

    return contiene_alguna(texto, palabras)


def es_compra(texto):
    palabras = [
        "quiero comprar",
        "comprar",
        "me interesa comprar",
        "quiero avanzar",
        "quiero senar",
        "senar",
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
        "me interesa ese",
        "me interesa esa",
        "ese me gusta",
        "esa me gusta",
        "quiero ese",
        "quiero esa",
    ]

    return contiene_alguna(texto, palabras)


#desde aca procesamos todas las palabras raras dentro del sistema lo que sea que no este del todo bien esto lo puede tomar como una intencion de respuesta o de "compra". la idea es siempre mantener el dialogo 











