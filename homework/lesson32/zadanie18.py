import asyncio

from aiohttp import web


async def chat(request):
    data = await request.json()
    prompt_text = data["prompt"]

    await asyncio.sleep(3)

    return web.json_response(
        {
            "response": (
                f"Otrzymałem twój prompt: '{prompt_text}' "
                "i przetworzyłem go."
            )
        }
    )


app = web.Application()

app.router.add_post("/api/v1/chat", chat)

web.run_app(app)
