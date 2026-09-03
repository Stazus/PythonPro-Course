import asyncio

from fastapi import FastAPI
from redis.asyncio import Redis


app = FastAPI()
redis = Redis(host="redis", port=6379, decode_responses=True)


@app.get("/data")
async def get_data():
    cached_data = await redis.get("data")

    if cached_data:
        return {
            "source": "cache",
            "data": cached_data,
        }

    await asyncio.sleep(2)
    data = "Dane pobrane z symulowanej bazy"

    await redis.set("data", data)

    return {
        "source": "database",
        "data": data,
    }
