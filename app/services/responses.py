import pandas as pd

from app.services.sheets import buscar_autos
from app.services.memory import usuarios
from app.services.conversation import (
    responder_financiacion,
    responder_permuta
)
from app.services.intents import ( 
    es_saludo,
    es_financiacion,
    es_permuta,
    es_fotos,
    parece_busqueda_auto #esto va a limpiarme el codigo porque esta hoja sera solo para que tenga las ordenes pero la intencion procesa palabras de todo tipo 
)

def generar_respuesta(sender_id, texto):

    texto = texto.lower().strip()

    # =========================
    # 1. SALUDOS
    # =========================

    if es_saludo(texto):

        return (
            "Hola 👋 Soy el asistente virtual de Zabaleo Motors 🚗\n"
            "¿Qué vehículo estás buscando?"
        )

    # =========================
    # 2. BUSCAR AUTOS
    # =========================

    autos = buscar_autos(texto)

    if len(autos) > 0:

        usuarios[sender_id] = {
            "ultimo_modelo": texto,
            "estado": "esperando_interes"
        }

        respuesta = "Encontré estos vehículos 🚗\n\n"

        for _, auto in autos.iterrows():

            # =========================
            # LIMPIAR AÑO
            # =========================

            anio = auto["año"]

            if pd.notna(anio):
                anio_str = str(int(float(str(anio))))
            else:
                anio_str = "N/D"

            # =========================
            # LIMPIAR PRECIO
            # =========================

            precio = auto["precio_lista"] # aca me busca el precio de lista 

            if pd.notna(precio):
                precio_num = int(
                    str(precio)
                    .replace("$", "")
                    .replace(".", "")
                    .replace(",", "")
                    .strip()
                )

                precio = f"${precio_num:,}".replace(",", ".")
            else:
                precio = "Consultar"

            # =========================
            # LIMPIAR KM
            # =========================

            km = auto["km"]

            if pd.notna(km):
                km_num = int(
                    str(km)
                    .replace(".", "")
                    .replace(",00", "")
                    .strip()
                )

                km_str = f"{km_num:,}".replace(",", ".")
            else:
                km_str = "N/D"
            
            color = auto["color"] if pd.notna(auto["color"]) else "Consultar"
            # =========================
            # ARMAR RESPUESTA DEL AUTO
            # =========================

            respuesta += (
                f"🚗 {auto['marca']} {auto['modelo']}\n"
                f"📅 Año: {anio_str}\n"
                f"💵 Precio: {precio}\n"
                f"🎨 Color : {auto[color]}\n"
                f"⚙️ Transmisión: {auto['transmision']}\n"
                f"⛽ Combustible: {auto['combustible']}\n"  
                f"🛣️ KM: {km_str}\n\n"
            )

        respuesta += (
            "👉 ¿Cuál te interesa más?\n"
            "Puedo ayudarte con financiación, permutas o más fotos."
        )

        return respuesta

    # =========================
    # 3. USUARIO EN CONVERSACION
    # =========================

    if sender_id in usuarios:

        estado = usuarios[sender_id]["estado"]

        if estado == "esperando_interes":

            if es_financiacion(texto):

                return responder_financiacion()

            elif  es_permuta(texto):

                return responder_permuta()

            elif  es_fotos(texto):

                return (
                    "Te enviamos más fotos enseguida 📸\n"
                    "También puedo derivarte con un asesor si querés ver más detalles."
                )
            # =========================
            # 4. parece busqueda .  # Esto es lo que genera una intencion de compra mas adelante 
            # =========================
            if parece_busqueda_auto(texto):
                return (
                "No encontré ese vehículo disponible por ahora 😕.\n\n"
                "Pero puedo ayudarte a buscar una alternativa similar dentro del stock.\n"
                "Podés consultar por marca o modelo, por ejemplo:\n"
                "▫️ Toyota\n"
                "▫️ Fiat\n"
                "▫️ Jeep\n"
                "▫️ Chevrolet"
    )
    
 # =========================
    # 5. DEFAULT
    # =========================

    return (
        "No entendí bien tu consulta 😕\n"
        "Podés escribirme una marca o modelo, por ejemplo: Toyota, Fiat, Hilux o Cronos."
    )
#Primero:
#saludos
#intenciones
#conversación