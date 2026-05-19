import pandas as pd
from app.services.sheets import buscar_autos
from app.services.memory import usuarios
from app.services.conversation import (
    responder_financiacion,
    responder_permuta
) # Esta logica se puede dividir en dos import   from app.services.conversation import responder_financiacion # from app.services.conversation import responder_permuta

def generar_respuesta(sender_id, texto):

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
        usuarios[sender_id] = {
            "ultimo_modelo": texto,
            "estado": "esperando_interes"
}
            

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
         #=====================
    # USUARIO EN CONVERSACION
    # =====================

    if sender_id in usuarios:

        estado = usuarios[sender_id]["estado"]

        if estado == "esperando_interes":

            if "financi" in texto:
                return responder_financiacion()

            elif "permuta" in texto:
                return responder_permuta()
            
            elif "foto" in texto:
                return "Te enviamos mas fotos enseguida 📸 "
            
            else :
                return("Puedo ayudarte con : \n"
                       "▫️ Financiacion \n "
                       "▫️ Permutas \n "
                       "▫️ Mas Fotos ")
        return respuesta
            
    
    # =========================
    # DEFAULT
    # =========================

    return "No encontré vehículos con esa búsqueda 😕"
#Primero:
#saludos
#intenciones
#conversación