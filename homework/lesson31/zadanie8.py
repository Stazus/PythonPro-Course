import asyncio
import random


async def ping(host):
    await asyncio.sleep(random.uniform(0.1, 1.0))
    return f"Host {host} odpowiada"


async def main():
    hosty = [
        "google.com",
        "github.com",
        "python.org",
        "wikipedia.org",
        "example.com"
    ]

    wyniki = await asyncio.gather(
        *(ping(host) for host in hosty)
    )

    for wynik in wyniki:
        print(wynik)


asyncio.run(main())
