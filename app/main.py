from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.get("/")
async def home():
    return {"status": "online"}

@app.get("/webhook")
async def verify_webhook(request: Request):

    params = request.query_params

    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)

    return {"error": "Token inválido"}

@app.post("/webhook")
async def receive_message(request: Request):

    body = await request.json()

    print("Mensaje recibido:")
    print(body)

    try:

        entry = body["entry"][0]
        messaging = entry["messaging"][0]

        sender_id = messaging["sender"]["id"]

        if "message" in messaging:

            user_message = messaging["message"].get("text", "")

            send_message(
                sender_id,
                f"Hola 👋 recibimos tu mensaje: {user_message}"
            )

    except Exception as e:
        print("ERROR:")
        print(e)

    return {"status": "ok"}

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