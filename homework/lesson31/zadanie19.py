import asyncio


def czy_pierwsza(liczba):
    if liczba < 2:
        return False

    for dzielnik in range(2, int(liczba ** 0.5) + 1):
        if liczba % dzielnik == 0:
            return False

    return True


async def generator_liczb_pierwszych():
    liczba = 2

    while liczba <= 100:
        if czy_pierwsza(liczba):
            await asyncio.sleep(0.1)
            yield liczba

        liczba += 1


async def main():
    async for liczba in generator_liczb_pierwszych():
        print(liczba)


asyncio.run(main())
