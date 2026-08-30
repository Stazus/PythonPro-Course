from fastapi import APIRouter


router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/")
async def get_books():
    return [
        {"id": 1, "title": "Wiedzmin"},
        {"id": 2, "title": "Hobbit"},
    ]


@router.get("/{book_id}")
async def get_book(book_id: int):
    return {
        "id": book_id,
        "title": "Wiedzmin",
    }
