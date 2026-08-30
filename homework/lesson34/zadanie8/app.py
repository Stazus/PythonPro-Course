import asyncio
import websockets
import time


clients = set()


async def handler(websocket):
    start_time = time.time()
    clients.add(websocket)

    print("Klient połączony")

    try:
        async for message in websocket:
            for client in clients:
                await client.send(message)
    finally:
        clients.remove(websocket)

        end_time = time.time()
        connection_time = end_time - start_time

        print(f"Klient rozłączony. Czas połączenia: {connection_time:.2f} s")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serwer WebSocket działa na ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
