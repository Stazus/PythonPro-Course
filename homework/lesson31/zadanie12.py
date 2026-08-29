import asyncio
import random


async def zadanie(numer):
    czas = random.randint(1, 10)
    await asyncio.sleep(czas)
    return numer, czas


async def main():
    zadania = [
        asyncio.create_task(zadanie(i))
        for i in range(1, 6)
    ]

    zakonczone, oczekujace = await asyncio.wait(
        zadania,
        return_when=asyncio.FIRST_COMPLETED
    )

    pierwsze = next(iter(zakonczone))
    numer, czas = pierwsze.result()

    print(f"Pierwsze zakończyło się zadanie {numer}.")
    print(f"Czas uśpienia: {czas} s")


    for pozostale in oczekujace:
        pozostale.cancel()


asyncio.run(main())
