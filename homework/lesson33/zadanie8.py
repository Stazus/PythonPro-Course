from fastapi import FastAPI


app = FastAPI(
    title="Books API",
    description="Proste API do zarządzania książkami.",
)


@app.get("/books", tags=["Books"])
async def get_books():
    """
    Zwraca listę książek.

    Przykład odpowiedzi:
    [
        {"id": 1, "title": "Wiedzmin"}
    ]
    """
    return [
        {
            "id": 1,
            "title": "Wiedzmin",
        }
    ]


@app.get("/books/{book_id}", tags=["Books"])
async def get_book(book_id: int):
    """
    Zwraca książkę o podanym ID.

    Przykład:
    GET /books/1
    """
    return {
        "id": book_id,
        "title": "Wiedzmin",
    }
