import asyncio
import time


async def zadanie(opoznienie):
    await asyncio.sleep(opoznienie)


async def main():
    start = time.time()

    await asyncio.gather(
        zadanie(1),
        zadanie(4),
        zadanie(2),
    )

    koniec = time.time()

    print(f"Całkowity czas wykonania: {koniec - start:.2f} s")


asyncio.run(main())
