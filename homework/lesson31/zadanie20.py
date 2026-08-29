import asyncio
import random


async def zadanie():
    czas = random.randint(1, 5)
    print(f"Wylosowany czas działania: {czas} s")

    await asyncio.sleep(czas)

    return f"Zadanie zakończone po {czas} s"


async def main():
    try:
        wynik = await asyncio.wait_for(zadanie(), timeout=3)
        print(wynik)
    except asyncio.TimeoutError:
        print("Przekroczono limit czasu 3 sekund.")


asyncio.run(main())
