import asyncio
import websockets


rooms = {}


async def handler(websocket):
    room_name = None

    try:
        async for message in websocket:
            if message.startswith("/join "):
                room_name = message.split(" ", 1)[1]

                if room_name not in rooms:
                    rooms[room_name] = set()

                rooms[room_name].add(websocket)

                await websocket.send(f"Dołączono do pokoju: {room_name}")
                print(f"Klient dołączył do pokoju: {room_name}")

            elif room_name is None:
                await websocket.send("Najpierw dołącz do pokoju komendą /join nazwa_pokoju")

            else:
                for client in rooms[room_name]:
                    await client.send(message)

    finally:
        if room_name and websocket in rooms.get(room_name, set()):
            rooms[room_name].remove(websocket)

            if not rooms[room_name]:
                del rooms[room_name]

        print("Klient rozłączony")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serwer WebSocket działa na ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
