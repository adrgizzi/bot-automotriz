import pandas as pd
from app.services.sheets import buscar_autos
from app.services.memory import usuarios
from app.services.conversation import (
    responder_financiacion,
    responder_permuta
) # Esta logica se puede dividir en dos import   from app.services.conversation import responder_financiacion # from app.services.conversation import responder_permuta

def generar_respuesta(sender_id, texto):
    texto = texto.lower()

    # 1. PRIMERO verificar si el usuario ya está en conversación
    if sender_id in usuarios:
        estado = usuarios[sender_id]["estado"]
        if estado == "esperando_interes":
            if "financi" in texto:
                return responder_financiacion()
            elif "permuta" in texto:
                return responder_permuta()
            elif "foto" in texto:
                return "Te enviamos más fotos enseguida 📸"
            else:
                return (
                    "Puedo ayudarte con:\n"
                    "▫️ Financiación\n"
                    "▫️ Permutas\n"
                    "▫️ Más Fotos"
                )

    # 2. DESPUÉS saludos
    if "hola" in texto or "buenas" in texto:
        return (
            "Hola 👋 Soy el asistente virtual de Zabaleo Motors 🚗\n"
            "¿Qué vehículo estás buscando?"
        )

    # 3. DESPUÉS buscar autos
    autos = buscar_autos(texto)

    if len(autos) > 0:
        usuarios[sender_id] = {
            "ultimo_modelo": texto,
            "estado": "esperando_interes"
        }
        respuesta = "Encontré estos vehículos 🚗\n\n"
        for _, auto in autos.iterrows():

            anio = auto['año']
            anio_str = str(int(float(str(anio)))) if pd.notna(anio) else "N/D"

            precio = auto['precio_lista']
            if pd.notna(precio):
                precio_num = int(str(precio).replace("$", "").replace(".", "").replace(",", "").strip())
                precio = f"${precio_num:,}".replace(",", ".")
            else:
                precio = "Consultar"

            km = auto['km']
            if pd.notna(km):
                km_num = int(str(km).replace(".", "").replace(",00", ""))
                km_str = f"{km_num:,}".replace(",", ".")
            else:
                km_str = "N/D"

            respuesta += (
                f"🚗 {auto['marca']} {auto['modelo']}\n"
                f"📅 Año: {anio_str}\n"
                f"💵 Precio: {precio}\n"
                f"⚙️ Transmisión: {auto['transmision']}\n"
                f"⛽ Combustible: {auto['combustible']}\n"
                f"🛣️ KM: {km_str}\n\n"
            )

        respuesta += (
            "\n👉 ¿Cuál te interesa más?\n"
            "Puedo ayudarte con financiación, permutas o más fotos."
        )
        return respuesta

    # 4. DEFAULT
    return "No encontré vehículos con esa búsqueda 😕"
#Primero:
#saludos
#intenciones
#conversación