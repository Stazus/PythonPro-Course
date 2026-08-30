from fastapi import FastAPI

from routers import authors, books


app = FastAPI(
    title="Books and Authors API",
)


app.include_router(books.router)
app.include_router(authors.router)
