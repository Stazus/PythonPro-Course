from fastapi import APIRouter


router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get("/")
async def get_authors():
    return [
        {"id": 1, "name": "Andrzej Sapkowski"},
        {"id": 2, "name": "J.R.R. Tolkien"},
    ]


@router.get("/{author_id}")
async def get_author(author_id: int):
    return {
        "id": author_id,
        "name": "Andrzej Sapkowski",
    }
