import asyncio
import aiofiles


async def zapisz_log(numer, lock):
    tekst = f"Log z korutyny {numer}\n"

    async with lock:
        async with aiofiles.open("logi.txt", "a", encoding="utf-8") as plik:
            await plik.write(tekst)

    print(f"Zapisano: {tekst.strip()}")


async def main():
    lock = asyncio.Lock()

    zadania = [
        zapisz_log(i, lock)
        for i in range(1, 6)
    ]

    await asyncio.gather(*zadania)


asyncio.run(main())
