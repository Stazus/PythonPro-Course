from aiohttp import web


async def strona_powitalna(request):
    return web.Response(
        text="<h1>Witaj na mojej stronie!</h1>",
        content_type="text/html"
    )


app = web.Application()
app.router.add_get("/", strona_powitalna)

web.run_app(app)
