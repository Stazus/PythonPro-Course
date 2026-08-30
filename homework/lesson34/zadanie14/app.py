import asyncio
import jwt
import websockets


SECRET_KEY = "tajny-klucz-do-zadania-14-minimum-32-znaki"


async def handler(websocket):
    try:
        token = await websocket.recv()

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("username", "nieznany")

            print(f"Uwierzytelniono użytkownika: {username}")
            await websocket.send("Autoryzacja poprawna")

        except jwt.InvalidTokenError:
            print("Nieprawidłowy token — rozłączam klienta")
            await websocket.close()
            return

        async for message in websocket:
            print(f"{username}: {message}")
            await websocket.send(f"Odebrano: {message}")

    finally:
        print("Klient rozłączony")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serwer WebSocket działa na ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
