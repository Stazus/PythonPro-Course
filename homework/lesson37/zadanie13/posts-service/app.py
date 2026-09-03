from fastapi import FastAPI
import psycopg2
import time

app = FastAPI()


def get_connection():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host="posts-db",
                dbname="postsdb",
                user="postsuser",
                password="postspassword",
            )
        except psycopg2.OperationalError:
            time.sleep(2)
    raise Exception("Nie udało się połączyć z bazą posts-db")


@app.on_event("startup")
def startup():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.get("/posts")
def get_posts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, title FROM posts ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"id": row[0], "user_id": row[1], "title": row[2]}
        for row in rows
    ]
