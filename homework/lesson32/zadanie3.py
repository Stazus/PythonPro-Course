from aiohttp import web


async def strona_powitalna(request):
    return web.Response(
        text="<h1>Witaj na mojej stronie!</h1>",
        content_type="text/html"
    )


async def dynamiczne_powitanie(request):
    imie = request.match_info["imie"]
    return web.Response(text=f"Witaj, {imie}!")


app = web.Application()

app.router.add_get("/", strona_powitalna)
app.router.add_get("/witaj/{imie}", dynamiczne_powitanie)

web.run_app(app)
