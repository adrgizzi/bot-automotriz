from app.services.sheets import buscar_autos

def generar_respuesta(texto):

    texto = texto.lower() # Esto realiza el pasado automatico de cualquier saludo este bien o mal escrito 

    # =========================
    # SALUDOS
    # =========================

    if "hola" in texto or "buenas" in texto:

        return (
            "Hola 👋 Soy el asistente virtual de Zabaleo Motors 🚗\n"
            "¿Qué vehículo estás buscando?"
        )

    # =========================
    # BUSCAR AUTOS
    # =========================

    autos = buscar_autos(texto)

    if len(autos) > 0:

        respuesta = "Encontré estos vehículos 🚗\n\n"

        for _, auto in autos.iterrows():

            respuesta += (
            f"🚗 {auto['marca']} {auto['modelo']}\n"
            f"📅 Año: {int(auto['año'])}\n"
            f"💵 Precio: {int(auto['precio'])}\n"
            f"⚙️ Transmisión: {auto['transmisión']}\n"
            f"⛽ Combustible: {auto['combustible']}\n"
            f"🛣️ KM: {int(auto['km'])}\n\n"# con int convierto un float en un entero , le saca los decimales 
            #f"🏢 Agencia: {auto['agencia']}\n\n"
)
                
                
                
            

        respuesta += (
            "\n👉 ¿Cuál te interesa más?\n"
            "Puedo ayudarte con financiación, permutas o más fotos."
        )

        return respuesta

    # =========================
    # DEFAULT
    # =========================

    return "No encontré vehículos con esa búsqueda 😕"


#Primero:
#saludos
#intenciones
#conversación