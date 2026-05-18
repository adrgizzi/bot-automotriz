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
            
            # AÑO
            anio = auto['año']
            anio_str = str(int(float(str(anio)))) if pd.notna(anio) else "N/D"


            # ==========
            # LIMPIAR PRECIO
            # ==========

          # LIMPIAR PRECIO
            precio = auto['precio']
            if pd.notna(precio):
                precio = str(precio).replace("$", "").strip()
                # Convertir a número y formatear con puntos
                precio_num = int(str(precio).replace(".", "").replace(",", ""))
                precio = f"${precio_num:,}".replace(",", ".")
            else:
                precio = "Consultar"

# LIMPIAR KM
            km = auto['km']
            if pd.notna(km):
                km_num = int(str(km).replace(".", "").replace(",00", ""))
                km_str = f"{km_num:,}".replace(",", ".")
            else:
                km_str = "N/D"

            # ==========
            # RESPUESTA 
            # ==========

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

    # =========================
    # DEFAULT
    # =========================

    return "No encontré vehículos con esa búsqueda 😕"
#Primero:
#saludos
#intenciones
#conversación