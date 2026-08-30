from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import engine, get_db
from models import Author, Base, Book
from schemas import (
    AuthorCreate,
    AuthorResponse,
    BookCreate,
    BookResponse,
)


app = FastAPI(title="Authors and Books API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post(
    "/authors",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_author(
    author: AuthorCreate,
    db: AsyncSession = Depends(get_db),
):
    new_author = Author(name=author.name)

    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)

    return new_author


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    author = await db.get(Author, book.author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    new_book = Book(
        title=book.title,
        price=book.price,
        author_id=book.author_id,
    )

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    return new_book


@app.get(
    "/authors/{author_id}/books",
    response_model=list[BookResponse],
)
async def get_author_books(
    author_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )

    author = result.scalar_one_or_none()

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author.books
