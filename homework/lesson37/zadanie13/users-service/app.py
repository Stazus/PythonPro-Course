from fastapi import FastAPI
import psycopg2
import time

app = FastAPI()


def get_connection():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host="users-db",
                dbname="usersdb",
                user="usersuser",
                password="userspassword",
            )
        except psycopg2.OperationalError:
            time.sleep(2)
    raise Exception("Nie udało się połączyć z bazą users-db")


@app.on_event("startup")
def startup():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{"id": row[0], "name": row[1]} for row in rows]
