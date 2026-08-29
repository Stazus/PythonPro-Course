# Uwaga: endpoint api.coindesk.com podany w treści zadania
# obecnie nie rozwiązuje się w DNS, dlatego połączenie kończy się błędem.
import asyncio

import aiohttp


async def main():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            dane = await response.json()

            cena_usd = dane["bpi"]["USD"]["rate"]
            print(f"Cena Bitcoina w USD: {cena_usd}")


if __name__ == "__main__":
    asyncio.run(main())
