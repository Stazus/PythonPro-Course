import time
import uuid

from fastapi import FastAPI, Request


app = FastAPI(title="Middleware Logging API")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    log_message = (
        f"method={request.method} "
        f"path={request.url.path} "
        f"time={process_time:.4f}s "
        f"request_id={request_id}\n"
    )

    with open("requests.log", "a", encoding="utf-8") as file:
        file.write(log_message)

    response.headers["X-Request-ID"] = request_id

    return response


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/books")
async def get_books():
    return {
        "books": [
            "Wiedzmin",
            "Solaris",
        ]
    }
