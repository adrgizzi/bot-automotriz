from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os
import traceback
from app.services.responses import generar_respuesta
from app.services.messenger import send_message
from app.services.leads import guardar_conversacion


load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "").strip()

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "online"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    hub_mode = params.get("hub.mode")
    hub_verify_token = (params.get("hub.verify_token") or "").strip()
    hub_challenge = params.get("hub.challenge")
    
    print("VERIFY_TOKEN configurado:", bool(VERIFY_TOKEN))
    print("Largo VERIFY_TOKEN:", len(VERIFY_TOKEN))
    print("Largo token recibido:", len(hub_verify_token))
    
    
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)
    return {"error": "Token inválido"}

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
            respuesta = generar_respuesta(sender_id, user_message)

            try:
                guardar_conversacion(sender_id, user_message, respuesta)
                print("Conversación guardada en PostgreSQL ✅")
            except Exception as e:
                print(f"Error guardando conversación: {e}")

            send_message(sender_id, respuesta)
    
    except Exception as e: 
        print("ERROR:")
        traceback.print_exc()
    return {"status": "ok"}



