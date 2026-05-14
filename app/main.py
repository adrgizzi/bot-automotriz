from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "bot_automotriz_zabaleoMotors_2026"

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

    return {"status": "ok"}

