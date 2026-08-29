import asyncio
import time


async def zadanie1():
    await asyncio.sleep(2)
    print("Zadanie 1 zakończone")


async def zadanie2():
    await asyncio.sleep(1)
    print("Zadanie 2 zakończone")


async def main():
    start = time.perf_counter()

    await zadanie1()
    await zadanie2()

    koniec = time.perf_counter()
    print(f"Czas wykonania: {koniec - start:.2f} s")


asyncio.run(main())
