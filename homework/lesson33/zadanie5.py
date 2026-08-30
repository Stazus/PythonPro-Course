from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Book(BaseModel):
    title: str
    author: str


books = {}
next_id = 1


@app.get("/books")
async def get_books():
    return list(books.values())


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return books[book_id]


@app.post("/books")
async def create_book(book: Book):
    global next_id

    new_book = {
        "id": next_id,
        "title": book.title,
        "author": book.author,
    }

    books[next_id] = new_book
    next_id += 1

    return new_book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    del books[book_id]

    return {"message": "Book deleted"}
