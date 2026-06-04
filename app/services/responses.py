
from app.services.sheets import buscar_autos, obtener_autos
from app.services.memory import usuarios
from app.services.conversation import (# esto permite responder todo y es la hoja donde habla con el cliente .
    responder_financiacion,
    responder_permuta,
    responder_derivacion_asesor,
    responder_fotos
)
from app.services.intents import ( # principales interaciones programadas donde identifica que es lo que quiere ese usuario
    es_saludo,
    es_financiacion,
    es_permuta,
    es_fotos,
    parece_busqueda_auto,
    es_asesor,
    es_compra
)
from app.services.formatters import ( # esto formatea todo los numeros o palabras para que sea todo mas suave al conversar 
    formatear_precio,
    formatear_anio,
    formatear_km,
    formatear_color,
    limpiar_precio
)
from app.services.filters import extraer_precio_maximo


from app.services.leads import ( #esto fuarda toda la interaccion con el cliente 
    guardar_cliente,
    guardar_oportunidad
)

def generar_respuesta(sender_id, texto):

    texto = texto.lower().strip()

    # =========================
    # 0. RESET / REINICIAR
    # =========================

    if texto in ["reset", "reiniciar", "empezar de nuevo", "volver a empezar"]:

        if sender_id in usuarios:
            del usuarios[sender_id]

        return (
            "Listo, reinicié la conversación 🔄\n"
            "Podés buscar por marca, modelo, año, precio, color, combustible o transmisión."
        )
    
     # =========================
    # 1. Rrevisar si espera nombre o telefono
    # =========================
    
    if sender_id in usuarios:
       
        estado=usuarios[sender_id].get("estado")
        
        if estado == "esperando_nombre":
            
            usuarios[sender_id]["nombre"]=texto.title()
            usuarios[sender_id]["estado"]="esperando_telefono"
            
            return (f"Gracias {usuarios[sender_id]['nombre']} 💪🏻\n"
                    "¿Me pasàs tu telefono para que un asesor pueda contactarte?"
                    )
        
        if estado =="esperando_telefono":
            usuarios[sender_id]["telefono"]=texto
            usuarios[sender_id]["estado"]="lead_completo"
        
            nombre = usuarios[sender_id].get("nombre")
            modelo = usuarios[sender_id].get("ultimo_modelo")
            telefono = usuarios[sender_id].get("telefono")
            interes = usuarios[sender_id].get("interes")
            try:
                guardar_cliente(sender_id, nombre, telefono)
                guardar_oportunidad(sender_id, modelo, interes)
                print("Lead guardado en PostgreSQL ✅")

            except Exception as e:
                print(f"Error guardando lead en PostgreSQL: {e}")
            return (
                "Perfecto , Ya tengo tus datos ✅ \n\n"
                f"Nombre : {nombre}\n"
                f"Telefono : {telefono}\n"
                f"Interès : {interes}\n"
                f"Consulta : {modelo}\n\n"
                "Ahora te derivo con yn asesosr para continuar.😁 \n"
                + responder_derivacion_asesor(
                    modelo=modelo,
                    nombre =nombre,
                    telefono = telefono,
                    interes = interes 
                )
            )
    # =========================
    # 2. SALUDO
    # =========================

    if es_saludo(texto):

        return (
            "Hola 👋 Soy el asistente virtual de Zabaleo Motors 🚗\n "
            "¿Qué vehículo estás buscando? "
        )
    
        
    # =========================
    # 3. ASESOR DIRECTO
    # =========================

    if es_asesor(texto):

        modelo = None

        if sender_id in usuarios:
            modelo = usuarios[sender_id].get("ultimo_modelo")

        return responder_derivacion_asesor(modelo)

    # =========================
    # 4. INTENCION DE COMPRA
    # =========================

    if es_compra(texto):

        modelo = None

        if sender_id in usuarios:
            modelo = usuarios[sender_id].get("ultimo_modelo")
        usuarios[sender_id]={
            "estado":"esperando_nombre",
            "ultimo_modelo":modelo,
            "interes":"compra",
            "nombre":None,
            "telefono":None,
        }
        return ("Perfecto 🤩 \n"
                "Para derivarte con una asesor y avanazar mejor la consulta "
                "¿Me decìs tu nombre?")

    # =========================
    # 5. BUSCAR AUTOS
    # =========================

    autos = buscar_autos(texto)

    print(f"Consulta: {texto} | Resultados: {len(autos)}")

    presupuesto = extraer_precio_maximo(texto)

    # =========================
    # 5.1 PRESUPUESTO SIN RESULTADOS
    # =========================

    if presupuesto and len(autos) == 0:

        todos_los_autos = obtener_autos()

        todos_los_autos["precio_num"] = todos_los_autos["precio_lista"].apply(limpiar_precio)

        autos_validos = todos_los_autos[
            todos_los_autos["precio_num"].notna()
        ].sort_values("precio_num", ascending=True)

        if len(autos_validos) > 0:

            auto = autos_validos.iloc[0]

            precio = formatear_precio(auto["precio_lista"])
            anio_str = formatear_anio(auto["año"])
            color = formatear_color(auto["color"])

            presupuesto_formateado = f"${presupuesto:,}".replace(",", ".")

            usuarios[sender_id] = {
                "ultimo_modelo": f"{auto['marca']} {auto['modelo']}",
                "estado": "esperando_interes",
                "autos_mostrados": [auto.to_dict()]
            }

            return (
                f"Por ahora no encontré vehículos disponibles hasta {presupuesto_formateado} 😕.\n\n"
                "La opción más económica que tenemos actualmente es:\n\n"
                f"🚗 {auto['marca']} {auto['modelo']}\n"
                f"📅 Año: {anio_str}\n"
                f"💵 Precio: {precio}\n"
                f"🎨 Color: {color}\n\n"
                "También podemos ayudarte con financiación para acercarte a una opción disponible.\n"
                "Podés escribir “financiación” o “asesor”."
            )

    # =========================
    # 5.2 SI ENCONTRO AUTOS
    # =========================

    if len(autos) > 0:

        autos = autos.head(5)

        usuarios[sender_id] = {
            "ultimo_modelo": texto,
            "estado": "esperando_interes",
            "autos_mostrados": autos.to_dict("records")
        }

        respuesta = "Encontré estos vehículos 🚗\n\n"

        for _, auto in autos.iterrows():

            anio_str = formatear_anio(auto["año"])
            precio = formatear_precio(auto["precio_lista"])
            km_str = formatear_km(auto["km"])
            color = formatear_color(auto["color"])

            respuesta += (
                f"🚗 {auto['marca']} {auto['modelo']}\n"
                f"📅 Año: {anio_str}\n"
                f"💵 Precio: {precio}\n"
                f"🎨 Color: {color}\n"
                f"⚙️ Transmisión: {auto['transmision']}\n"
                f"⛽ Combustible: {auto['combustible']}\n"
                f"🛣️ KM: {km_str}\n\n"
            )

        respuesta += (
            "👉 ¿Cuál te interesa más?\n"
            "Puedo ayudarte con financiación, permutas, más fotos o derivarte con un asesor."
        )

        return respuesta

    # =========================
    # 6. USUARIO EN CONVERSACION
    # =========================

    if sender_id in usuarios:

        estado = usuarios[sender_id]["estado"]

        if estado == "esperando_interes":

            if es_financiacion(texto):

                return responder_financiacion()

            elif es_permuta(texto):

                return responder_permuta()

            elif es_fotos(texto):

                modelo = usuarios[sender_id].get("ultimo_modelo")

                return responder_fotos(modelo)

    # =========================
    # 7. PARECE BUSQUEDA PERO NO ENCONTRO NADA
    # =========================

    if parece_busqueda_auto(texto):

        return (
            "No encontré ese vehículo disponible por ahora 😕.\n\n"
            "Pero puedo ayudarte a buscar una alternativa similar dentro del stock.\n"
            "Podés consultar por marca o modelo, por ejemplo:\n"
            "▫️ Toyota\n"
            "▫️ Fiat\n"
            "▫️ Jeep\n"
            "▫️ Cruze\n"
            "▫️ Hilux\n"
            "▫️ Raptor"
        )

    # =========================
    # 8. DEFAULT
    # =========================

    return (
        "No entendí bien tu consulta 😕\n"
        "Podés escribirme una marca o modelo, por ejemplo: Toyota, Fiat, Hilux o Cronos."
    )
#Primero:
#saludos
#intenciones
#conversación

#"""El orden : 
#0. reset
#1. revisar si está esperando nombre o teléfono
#2. saludo
#3. asesor directo
#4. intención de compra
#5. buscar autos
#6. conversación activa financiación / permuta / fotos
#7. presupuesto / no encontrado
#8. default