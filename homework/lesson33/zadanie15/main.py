from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_db
from models import Base, Book
from schemas import BookCreate, BookResponse


app = FastAPI(title="Books Background Tasks API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def send_email_log(book_title: str):
    with open("email.log", "a", encoding="utf-8") as file:
        file.write(
            f'Email sent: book "{book_title}" was created.\n'
        )


def update_statistics():
    with open("statistics.log", "a", encoding="utf-8") as file:
        file.write("Statistics updated after deleting a book.\n")


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book: BookCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    new_book = Book(
        title=book.title,
        author=book.author,
        price=book.price,
    )

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    background_tasks.add_task(
        send_email_log,
        new_book.title,
    )

    return new_book


@app.get(
    "/books",
    response_model=list[BookResponse],
)
async def get_books(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Book))
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

    await db.commit()
    await db.refresh(book)

    return book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_id: int,
    background_tasks: BackgroundTasks,
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

    background_tasks.add_task(
        update_statistics
    )
