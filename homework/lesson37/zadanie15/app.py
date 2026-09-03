from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import time
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Łączna liczba requestów HTTP",
    ["method", "endpoint"],
)


class Book(BaseModel):
    title: str
    author: str


def get_connection():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host="database",
                dbname="booksdb",
                user="booksuser",
                password="bookspassword",
            )
        except psycopg2.OperationalError:
            time.sleep(2)

    raise Exception("Nie udało się połączyć z bazą danych")


@app.on_event("startup")
def startup():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL
        )
        """
    )

    conn.commit()
    cur.close()
    conn.close()


@app.get("/books")
def get_books():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, author FROM books ORDER BY id")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"id": row[0], "title": row[1], "author": row[2]}
        for row in rows
    ]


@app.post("/books")
def create_book(book: Book):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO books (title, author) VALUES (%s, %s) RETURNING id",
        (book.title, book.author),
    )

    book_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": book_id,
        "title": book.title,
        "author": book.author,
    }


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE books
        SET title = %s, author = %s
        WHERE id = %s
        RETURNING id
        """,
        (book.title, book.author, book_id),
    )

    updated = cur.fetchone()

    if updated is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Książka nie istnieje")

    conn.commit()
    cur.close()
    conn.close()

    return {
        "id": book_id,
        "title": book.title,
        "author": book.author,
    }


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM books WHERE id = %s RETURNING id",
        (book_id,),
    )

    deleted = cur.fetchone()

    if deleted is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Książka nie istnieje")

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Książka została usunięta"}

@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
    ).inc()

    return response

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

