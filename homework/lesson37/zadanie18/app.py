import asyncio

import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

REDIS_URL = "redis://redis:6379"
CHANNEL = "chat"


@app.get("/")
async def index():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>WebSocket Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>

        <input id="message" placeholder="Wpisz wiadomość">
        <button onclick="sendMessage()">Wyślij</button>

        <ul id="messages"></ul>

        <script>
            const wsProtocol = location.protocol === "https:" ? "wss" : "ws";
            const ws = new WebSocket(
                wsProtocol + "://" + location.host + "/ws"
            );

            ws.onmessage = function(event) {
                const li = document.createElement("li");
                li.textContent = event.data;
                document.getElementById("messages").appendChild(li);
            };

            function sendMessage() {
                const input = document.getElementById("message");
                ws.send(input.value);
                input.value = "";
            }
        </script>
    </body>
    </html>
    """)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    publisher = redis.from_url(REDIS_URL, decode_responses=True)
    subscriber = redis.from_url(REDIS_URL, decode_responses=True)

    pubsub = subscriber.pubsub()
    await pubsub.subscribe(CHANNEL)

    async def send_messages():
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])

    sender_task = asyncio.create_task(send_messages())

    try:
        while True:
            data = await websocket.receive_text()
            await publisher.publish(CHANNEL, data)

    except WebSocketDisconnect:
        sender_task.cancel()

    finally:
        await pubsub.unsubscribe(CHANNEL)
        await pubsub.close()
        await publisher.close()
        await subscriber.close()
