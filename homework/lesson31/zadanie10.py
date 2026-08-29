import asyncio


async def odliczanie(nazwa, start):
    for pozostalo in range(start, 0, -1):
        print(f"{nazwa}: zostało {pozostalo} sekund")
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(
        odliczanie("Odliczanie 1", 5),
        odliczanie("Odliczanie 2", 3),
        odliczanie("Odliczanie 3", 7)
    )


asyncio.run(main())
