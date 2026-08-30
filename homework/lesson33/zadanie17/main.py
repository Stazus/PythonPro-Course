import json
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from database import engine
from models import Base


app = FastAPI(title="Startup and Shutdown Events API")

CACHE_FILE = Path("cache.json")
cache: dict = {}


@app.on_event("startup")
async def startup_event():
    global cache

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            cache = json.load(file)
    else:
        cache = {}

    print("Startup: database initialized and cache loaded")


@app.on_event("shutdown")
async def shutdown_event():
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=4)

    await engine.dispose()

    print("Shutdown: cache saved and database connection closed")


@app.get("/cache")
async def get_cache():
    return cache


@app.post("/cache/{key}/{value}")
async def set_cache_value(key: str, value: str):
    cache[key] = value

    return {
        "message": "Cache updated",
        "cache": cache,
    }
