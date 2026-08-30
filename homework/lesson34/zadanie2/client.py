import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://localhost:8080/ws") as ws:
            messages = [
                "Cześć",
                "Jak się masz?",
                "Do widzenia",
            ]

            for message in messages:
                await ws.send_str(message)
                response = await ws.receive()
                print(response.data)


asyncio.run(main())
