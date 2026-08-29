from aiohttp import web


async def home(request):
    return web.Response(text="Strona główna")


async def info(request):
    return web.Response(text="Informacje")


def setup_routes(app):
    app.router.add_get("/", home)
    app.router.add_get("/info", info)
