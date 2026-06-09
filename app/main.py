from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os
import traceback
from app.services.responses import generar_respuesta
from app.services.messenger import send_message
from app.services.leads import guardar_conversacion


load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "").strip() # strip sirve para dar espacio 

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
    
    verify_token_configurado = (VERIFY_TOKEN or "").strip()
    
    print("VERIFY_TOKEN existe:", bool(verify_token_configurado))
    print("Largo VERIFY_TOKEN:", len(verify_token_configurado))
    print("Largo token recibido:", len(hub_verify_token))
    print("Tokens coinciden:", hub_verify_token == verify_token_configurado)

    
    if hub_mode == "subscribe" and hub_verify_token == verify_token_configurado:
        return PlainTextResponse(content=hub_challenge)
    return {"error": "Token inválido"}
@app.get("/debug-db")
async def debug_db():
    try:
        guardar_conversacion(
            "debug_railway",
            "prueba directa desde railway",
            "ok"
        )

        return {
            "ok": True,
            "database_url_exists": bool(os.getenv("DATABASE_URL"))
        }

    except Exception as e:
        return {
            "ok": False,
            "database_url_exists": bool(os.getenv("DATABASE_URL")),
            "error": str(e)
        }   
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



