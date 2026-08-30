import asyncio
import websockets


clients = set()


async def handler(websocket):
    clients.add(websocket)

    try:
        nick = await websocket.recv()
        print(f"Dołączył użytkownik: {nick}")

        async for message in websocket:
            full_message = f"{nick}: {message}"

            for client in clients:
                await client.send(full_message)

    finally:
        clients.remove(websocket)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serwer WebSocket działa na ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
