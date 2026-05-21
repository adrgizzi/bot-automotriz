def responder_financiacion():
    return (
        "💳 Trabajamos con opciones de financiación sujetas a aprobación.\n\n"
        "El monto de cuotas y anticipo depende del vehículo y del perfil crediticio.\n\n"
        "Si querés, puedo derivarte con un asesor para evaluar las opciones disponibles.\n"
        "Escribí: asesor"
    )


def responder_permuta():
    return (
        "🚘 Tomamos vehículos en parte de pago.\n\n"
        "La cotización depende del modelo, año, kilometraje y estado general del vehículo.\n\n"
        "Si querés, puedo derivarte con un asesor para evaluar tu unidad.\n"
        "Escribí: asesor"
    )

def responder_derivacion_asesor(modelo=None):
    numero_whatsapp = "5493512201289"  # reemplazar por el número real

    mensaje = "Hola, vengo desde el bot de Zabaleo Motors"

    if modelo:
        mensaje += f" y estoy consultando por {modelo}"

    mensaje_url = mensaje.replace(" ", "%20")

    return (
        "Perfecto 😊\n"
        "Te puedo derivar con un asesor para continuar la consulta.\n\n"
        f"📲 Escribinos por WhatsApp acá:\n"
        f"https://wa.me/{numero_whatsapp}?text={mensaje_url}"
    )
    
def responder_fotos(modelo=None):
    numero_whatsapp = "5493512201289"  # Numero real , No enviar a ningun otro lugar 

    mensaje = "Hola, vengo desde el bot de Zabaleo Motors y quiero ver fotos"

    if modelo:
        mensaje += f" de {modelo}"

    mensaje_url = mensaje.replace(" ", "%20")

    return (
        "Perfecto 📸\n"
        "Para enviarte fotos reales de la unidad exacta, te derivo con un asesor.\n\n"
        "📲 Escribinos por WhatsApp acá:\n"
        f"https://wa.me/{numero_whatsapp}?text={mensaje_url}"
    )