from aiohttp import web


async def echo(request):
    dane = await request.json()
    return web.json_response(dane)


app = web.Application()
app.router.add_post("/api/echo", echo)

web.run_app(app)
