from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Bot automotriz funcionando"}

@app.get("/webhook")
async def verify_webhook(request: Request):

    params = request.query_params

    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    VERIFY_TOKEN = "mi_token_secreto"

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return {"error": "Token inválido"}

@app.post("/webhook")
async def receive_message(request: Request):

    body = await request.json()

    print("Mensaje recibido:")
    print(body)

    return {"status": "ok"}