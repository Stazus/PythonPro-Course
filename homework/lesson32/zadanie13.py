import asyncio

import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/todos/2",
        "https://jsonplaceholder.typicode.com/todos/3",
    ]

    async with aiohttp.ClientSession() as session:
        wyniki = await asyncio.gather(
            *(fetch(session, url) for url in urls)
        )

    for wynik in wyniki:
        print(wynik)


if __name__ == "__main__":
    asyncio.run(main())
