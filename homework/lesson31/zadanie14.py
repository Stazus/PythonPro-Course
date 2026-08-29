import asyncio


async def producent(kolejka):
    for liczba in range(1, 21):
        await asyncio.sleep(0.5)
        await kolejka.put(liczba)
        print(f"Producent dodał: {liczba}")


async def konsument(nazwa, kolejka):
    while True:
        liczba = await kolejka.get()

        print(f"{nazwa} przetworzył liczbę: {liczba}")

        kolejka.task_done()


async def main():
    kolejka = asyncio.Queue()

    zadanie_producenta = asyncio.create_task(
        producent(kolejka)
    )

    konsumenci = [
        asyncio.create_task(konsument("Konsument 1", kolejka)),
        asyncio.create_task(konsument("Konsument 2", kolejka))
    ]

    await zadanie_producenta
    await kolejka.join()

    for konsument_task in konsumenci:
        konsument_task.cancel()


asyncio.run(main())
