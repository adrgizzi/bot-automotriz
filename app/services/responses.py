from app.services.sheets import buscar_autos

def generar_respuesta(texto):

    autos = buscar_autos(texto) 

    if not autos.empty:

        respuesta = "Encontré estos vehículos 🚗\n\n"

        for _, auto in autos.iterrows():

            respuesta += (
                f"{auto['marca']} "
                f"{auto['modelo']} "
                f"{auto['año']} - "
                f"USD {auto['precio']}\n"
                f"{auto['transmisión']} - "
                f"{auto['combustible']}\n"
                f"{auto['km']} km\n"
                f"Agencia: {auto['agencia']}\n\n"
            )

        return respuesta

    return "No encontré vehículos con esa búsqueda 😕"