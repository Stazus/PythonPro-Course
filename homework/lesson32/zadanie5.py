from aiohttp import web


async def search(request):
    q = request.query.get("q")

    if q:
        return web.json_response({
            "szukana_fraza": q
        })

    return web.json_response({
        "błąd": "Brak parametru q"
    })


app = web.Application()
app.router.add_get("/api/search", search)

web.run_app(app)
