import asyncio


async def pobierz_pogode(miasto):
    await asyncio.sleep(1.5)

    return {
        "miasto": miasto,
        "temperatura": 25,
        "stan": "słonecznie"
    }


async def main():
    miasta = ["Warszawa", "Kraków", "Gdańsk"]

    wyniki = await asyncio.gather(
        *(pobierz_pogode(miasto) for miasto in miasta)
    )

    for wynik in wyniki:
        print(wynik)


asyncio.run(main())
