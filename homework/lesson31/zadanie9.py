import asyncio
import aiohttp


async def sprawdz_status(session, url):
    try:
        async with session.get(url) as odpowiedz:
            return f"{url} - Status: {odpowiedz.status}"
    except aiohttp.ClientError as blad:
        return f"{url} - Błąd: {blad}"


async def main():
    adresy = [
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://wikipedia.org",
        "https://example.com"
    ]

    async with aiohttp.ClientSession() as session:
        wyniki = await asyncio.gather(
            *(sprawdz_status(session, url) for url in adresy)
        )

    for wynik in wyniki:
        print(wynik)


asyncio.run(main())
