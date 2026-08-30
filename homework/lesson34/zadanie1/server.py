from aiohttp import web


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(f"Server: {msg.data}")

        elif msg.type == web.WSMsgType.ERROR:
            print(f"WebSocket error: {ws.exception()}")

    return ws


app = web.Application()
app.router.add_get("/ws", websocket_handler)


if __name__ == "__main__":
    web.run_app(app, host="localhost", port=8080)
