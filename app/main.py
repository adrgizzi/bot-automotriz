from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os
import requests
import traceback

# =========================
# CARGAR VARIABLES ENTORNO
# =========================

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

# =========================
# FASTAPI
# =========================

app = FastAPI()

# =========================
# FUNCION ENVIAR MENSAJE
# =========================

def send_message(recipient_id, message_text):

    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("RESPUESTA META:")
    print(response.status_code)
    print(response.text)

# =========================
# HOME
# =========================

@app.get("/")
async def home():

    return {
        "status": "online"
    }

# =========================
# VERIFICACION WEBHOOK META
# =========================

@app.get("/webhook")
async def verify_webhook(request: Request):

    params = request.query_params

    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:

        return PlainTextResponse(content=hub_challenge)

    return {
        "error": "Token inválido"
    }

# =========================
# RECIBIR MENSAJES
# =========================

@app.post("/webhook")
async def receive_message(request: Request):

    body = await request.json()

    print("MENSAJE RECIBIDO:")
    print(body)

    try:

        entry = body["entry"][0]
        messaging = entry["messaging"][0]

        sender_id = messaging["sender"]["id"]

        if "message" in messaging:

            user_message = messaging["message"].get("text", "")

            print("USUARIO:")
            print(user_message)

            texto = user_message.lower()

            # =========================
            # RESPUESTAS BOT
            # =========================

            if "hola" in texto:

                send_message(
                    sender_id,
                    "Hola 👋 Soy el asistente virtual de Zabaleo Motors 🚗\n¿Qué vehículo estás buscando?"
                )

            elif "hilux" in texto:

                send_message(
                    sender_id,
                    "Tenemos Toyota Hilux disponibles 🔥\n¿Buscás automática o manual?"
                )

            elif "amarok" in texto:

                send_message(
                    sender_id,
                    "Tenemos Volkswagen Amarok disponibles 🚗\n¿Querés ver modelos o precios?"
                )

            elif "financiación" in texto or "financiacion" in texto:

                send_message(
                    sender_id,
                    "Sí 👍 trabajamos con opciones de financiación.\n¿De qué vehículo querés información?"
                )

            else:

                send_message(
                    sender_id,
                    "Perfecto 👍 Contame qué vehículo estás buscando y te ayudamos."
                )

    except Exception as e:

        print("ERROR:")
        traceback.print_exc()

    return {
        "status": "ok"
    }