import asyncio
import time


class RateLimiter:
    def __init__(self, limit):
        self.limit = limit
        self.odstep = 1 / limit
        self.ostatnie_wywolanie = 0
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            teraz = time.monotonic()
            czas_oczekiwania = self.odstep - (teraz - self.ostatnie_wywolanie)

            if czas_oczekiwania > 0:
                await asyncio.sleep(czas_oczekiwania)

            self.ostatnie_wywolanie = time.monotonic()


async def zadanie(numer, limiter):
    await limiter.acquire()
    print(f"Zadanie {numer} wykonane o {time.strftime('%H:%M:%S')}")


async def main():
    limiter = RateLimiter(5)

    zadania = [
        asyncio.create_task(zadanie(i, limiter))
        for i in range(1, 21)
    ]

    await asyncio.gather(*zadania)


asyncio.run(main())
