from aiohttp import web


active_connections = 0


async def websocket_handler(request):
    global active_connections

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    active_connections += 1
    await ws.send_str(f"Jesteś klientem numer {active_connections}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                await ws.send_str(f"Server: {msg.data}")

            elif msg.type == web.WSMsgType.ERROR:
                print(f"WebSocket error: {ws.exception()}")

    finally:
        active_connections -= 1

    return ws


app = web.Application()
app.router.add_get("/ws", websocket_handler)


if __name__ == "__main__":
    web.run_app(app, host="localhost", port=8080)
