import pandas as pd


def limpiar_precio(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    valor = valor.replace("$", "").replace(" ", "")

    if "," in valor:
        valor = valor.split(",")[0]

    valor = valor.replace(".", "")

    try:
        return int(valor)
    except ValueError:
        return None


def formatear_precio(valor):
    precio_num = limpiar_precio(valor)

    if precio_num is not None:
        return f"${precio_num:,}".replace(",", ".")

    return "Consultar"