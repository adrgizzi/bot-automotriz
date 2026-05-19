import pandas as pd

from app.services.sheets import buscar_autos
from app.services.memory import usuarios
from app.services.conversation import (
    responder_financiacion,
    responder_permuta
)


def generar_respuesta(sender_id, texto):

    texto = texto.lower().strip()

    # =========================
    # 1. SALUDOS
    # =========================

    if "hola" in texto or "buenas" in texto:

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

            # =========================
            # ARMAR RESPUESTA DEL AUTO
            # =========================

            respuesta += (
                f"🚗 {auto['marca']} {auto['modelo']}\n"
                f"📅 Año: {anio_str}\n"
                f"💵 Precio: {precio}\n"
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

            if "financi" in texto:

                return responder_financiacion()

            elif "permuta" in texto:

                return responder_permuta()

            elif "foto" in texto:

                return (
                    "Te enviamos más fotos enseguida 📸\n"
                    "También puedo derivarte con un asesor si querés ver más detalles."
                )

            else:

                return (
                    "Puedo ayudarte con:\n"
                    "▫️ Financiación\n"
                    "▫️ Permutas\n"
                    "▫️ Más fotos\n\n"
                    "Decime qué opción te interesa."
                )

    # =========================
    # 4. DEFAULT
    # =========================

    return (
        "No encontré vehículos con esa búsqueda 😕\n"
        "Probá escribiendo una marca o modelo, por ejemplo: Fiat, Toyota, Hilux, Cronos."
    )
#Primero:
#saludos
#intenciones
#conversación