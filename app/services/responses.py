from app.services.sheets import buscar_autos

def generar_respuesta(texto):

    autos = buscar_autos(texto)
    
    if "hola" in texto or "buenas" in texto:
        return (
        "Hola 👋 Soy el asistente virtual de Zabaleo Motors 🚗\n"
        "¿Qué vehículo estás buscando?"
    )

    if len(autos) > 0:

        respuesta = "Encontré estos vehículos 🚗\n\n"

        for _, auto in autos.iterrows():

            respuesta += (
             f"🚗 {auto['marca']} {auto['modelo']}\n"
            f"📅 Año: {auto['año']}\n"
            f"💵 Precio: USD {auto['precio']}\n"
            f"⚙️ Transmisión: {auto['transmisión']}\n"
            f"⛽ Combustible: {auto['combustible']}\n"
            f"🛣️ KM: {auto['km']}\n" 
            f"🏢 Agencia: {auto['agencia']}\n\n"# con el doble separa modelo a modelo 
            
)
            respuesta += (
             "\n👉 ¿Cuál te interesa más?\n"
            "Puedo ayudarte con financiación, permutas o más fotos."
)
        return respuesta

    return "No encontré vehículos con esa búsqueda 😕"
