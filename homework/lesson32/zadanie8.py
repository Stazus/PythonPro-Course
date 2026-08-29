from aiohttp import web


async def witaj(request):
    imie = request.match_info["imie"]

    if imie == "admin":
        raise web.HTTPForbidden(text="Dostęp dla admina zabroniony")

    return web.Response(text=f"Witaj, {imie}!")


app = web.Application()
app.router.add_get("/witaj/{imie}", witaj)

web.run_app(app)
