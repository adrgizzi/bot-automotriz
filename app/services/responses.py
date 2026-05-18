from app.services.sheets import buscar_autos

def generar_respuesta(texto):

    autos = buscar_autos(texto)

    if len(autos) > 0:

        respuesta = "Encontré estos vehículos 🚗\n\n"

        for _, auto in autos.iterrows():

            respuesta += (
                f"{auto['marca']} "
                f"{auto['modelo']} "
                f"{auto['año']} - "
                f"{auto['precio']} - "
                f"Transmision {auto['transmisión']} - "
                f"Combustible {auto['combustible']} - "
                f"Kilometros {auto['km']}\n"
            )

        return respuesta

    return "No encontré vehículos con esa búsqueda 😕"
