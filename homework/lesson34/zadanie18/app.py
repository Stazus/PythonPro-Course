from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


app = FastAPI()

connections = {}


class Notification(BaseModel):
    user: str
    message: str


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    connections[username] = websocket

    print(f"Połączono użytkownika: {username}")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.pop(username, None)
        print(f"Rozłączono użytkownika: {username}")


@app.post("/notifications")
async def create_notification(notification: Notification):
    websocket = connections.get(notification.user)

    if websocket:
        await websocket.send_json({
            "message": notification.message
        })

        return {
            "status": "sent",
            "user": notification.user
        }

    return {
        "status": "offline",
        "user": notification.user
    }
