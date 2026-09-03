from aiohttp import web


async def hello(request):
    return web.Response(text="Hello from Docker!")


app = web.Application()
app.router.add_get("/", hello)

web.run_app(app, host="0.0.0.0", port=8000)
