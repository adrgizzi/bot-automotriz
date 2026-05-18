from app.services.sheets import buscar_autos

def generar_respuesta(texto):

    autos = buscar_autos(texto)

    if len(autos) > 0:

        respuesta = "Encontré estos vehículos 🚗\n\n"

        for _, auto in autos.iterrows():

            respuesta += (
             f"🚗 {auto['marca']} {auto['modelo']}\n"
            f"📅 Año: {auto['año']}\n"
            f"💵 Precio: USD {auto['precio']}\n"
            f"⚙️ Transmisión: {auto['transmisión']}\n"
            f"⛽ Combustible: {auto['combustible']}\n"
            f"🛣️ KM: {auto['km']}\n\n" # con el doble separa modelo a modelo 
            
)

        return respuesta

    return "No encontré vehículos con esa búsqueda 😕"
