from datetime import datetime
import random

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/time")
async def get_time():
    return {"time": datetime.now().isoformat()}


@app.get("/random")
async def get_random():
    return {"random": random.randint(1, 100)}
