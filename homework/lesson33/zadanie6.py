from fastapi import FastAPI, HTTPException, Response, status
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return books[book_id]


@app.post("/books", status_code=status.HTTP_201_CREATED)
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


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    del books[book_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
