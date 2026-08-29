from aiohttp import web
from datetime import datetime


async def status(request):
    return web.json_response({
        "status": "OK",
        "server_time": str(datetime.now())
    })


app = web.Application()
app.router.add_get("/api/status", status)

web.run_app(app)
