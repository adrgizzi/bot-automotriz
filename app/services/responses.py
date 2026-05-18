import pandas as pd
from app.services.sheets import buscar_autos


def generar_respuesta(texto):

    texto = texto.lower()

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

            # ==========
            # LIMPIAR PRECIO
            # ==========

            precio = auto['precio']

            if pd.notna(precio):

                precio = str(precio)
                precio = precio.replace("$", "")
                precio = precio.replace(".", "")
                precio = precio.strip()

            else:
                precio = "Consultar"

            # ==========
            # VARIABLES
            # ==========

            anio = auto['año']
            km = auto['km']

            # ==========
            # RESPUESTA
            # ==========

            respuesta += (
                f"🚗 {auto['marca']} {auto['modelo']}\n"
                f"📅 Año: {int(anio) if pd.notna(anio) else 'N/D'}\n"
                f"💵 Precio: {precio}\n"
                f"⚙️ Transmision: {auto['transmisión']}\n"
                f"⛽ Combustible: {auto['combustible']}\n"
                f"🛣️ KM: {int(km) if pd.notna(km) else 'N/D'}\n\n"
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