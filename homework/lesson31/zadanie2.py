import asyncio


async def licznik(n):
    for liczba in range(1, n + 1):
        print(liczba)
        await asyncio.sleep(1)


asyncio.run(licznik(5))
