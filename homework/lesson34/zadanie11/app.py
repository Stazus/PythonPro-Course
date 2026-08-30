import asyncio
import time
import websockets


async def handler(websocket):
    last_pong = time.time()

    async def ping_loop():
        nonlocal last_pong

        while True:
            await asyncio.sleep(30)

            if time.time() - last_pong > 60:
                print("Brak pong przez 60 sekund — rozłączam klienta")
                await websocket.close()
                break

            print("Wysyłam: ping")
            await websocket.send("ping")

    ping_task = asyncio.create_task(ping_loop())

    try:
        async for message in websocket:
            if message == "pong":
                last_pong = time.time()
                print("Odebrano: pong")
    finally:
        ping_task.cancel()
        print("Klient rozłączony")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serwer WebSocket działa na ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
