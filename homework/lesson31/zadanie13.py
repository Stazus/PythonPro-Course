import asyncio


async def obsluz_klienta(reader, writer):
    dane = await reader.read(100)
    wiadomosc = dane.decode()

    print(f"Odebrano: {wiadomosc}")

    writer.write(dane)
    await writer.drain()

    print(f"Odesłano: {wiadomosc}")

    writer.close()
    await writer.wait_closed()


async def main():
    serwer = await asyncio.start_server(
        obsluz_klienta,
        "localhost",
        8888
    )

    print("Serwer działa na localhost:8888")

    async with serwer:
        await serwer.serve_forever()


asyncio.run(main())
