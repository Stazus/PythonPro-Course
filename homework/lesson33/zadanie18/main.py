from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_db
from models import Base, Book
from schemas import BookCreate, BookResponse


app = FastAPI(title="Books Pagination and Filtering API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    new_book = Book(
        title=book.title,
        author=book.author,
        price=book.price,
        category=book.category,
    )

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    return new_book


@app.get(
    "/books",
    response_model=list[BookResponse],
)
async def get_books(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    category: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    sort_by: Literal["price", "title"] | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Book)

    if category is not None:
        query = query.where(Book.category == category)

    if min_price is not None:
        query = query.where(Book.price >= min_price)

    if max_price is not None:
        query = query.where(Book.price <= max_price)

    if sort_by == "price":
        query = query.order_by(asc(Book.price))

    if sort_by == "title":
        query = query.order_by(asc(Book.title))

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book


@app.put(
    "/books/{book_id}",
    response_model=BookResponse,
)
async def update_book(
    book_id: int,
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    book.title = book_data.title
    book.author = book_data.author
    book.price = book_data.price
    book.category = book_data.category

    await db.commit()
    await db.refresh(book)

    return book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    await db.delete(book)
    await db.commit()
