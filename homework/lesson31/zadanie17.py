import asyncio
import time


async def pobierz_id_uzytkownika(nazwa_uzytkownika):
    await asyncio.sleep(1)
    return 123


async def pobierz_posty(id_uzytkownika):
    await asyncio.sleep(1)
    return [101, 102, 103, 104, 105]


async def pobierz_komentarze(id_postu):
    await asyncio.sleep(1)
    return [
        f"Komentarz 1 do posta {id_postu}",
        f"Komentarz 2 do posta {id_postu}",
    ]


async def main():
    start = time.perf_counter()

    nazwa_uzytkownika = "stanislaw"

    id_uzytkownika = await pobierz_id_uzytkownika(nazwa_uzytkownika)
    print(f"ID użytkownika: {id_uzytkownika}")

    posty = await pobierz_posty(id_uzytkownika)
    print(f"Posty użytkownika: {posty}")

    zadania = [
        pobierz_komentarze(id_postu)
        for id_postu in posty
    ]

    komentarze = await asyncio.gather(*zadania)

    for id_postu, lista_komentarzy in zip(posty, komentarze):
        print(f"Post {id_postu}: {lista_komentarzy}")

    koniec = time.perf_counter()

    print(f"Czas wykonania: {koniec - start:.2f} s")


asyncio.run(main())
