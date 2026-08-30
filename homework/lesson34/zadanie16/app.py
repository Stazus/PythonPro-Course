import asyncio
import sqlite3
import websockets


DB_NAME = "chat.db"
clients = set()


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)


def save_message(message):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO messages (content) VALUES (?)",
            (message,)
        )


def get_last_messages(limit=50):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            """
            SELECT content
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        messages = [row[0] for row in cursor.fetchall()]
        messages.reverse()

        return messages


async def handler(websocket):
    clients.add(websocket)

    try:
        history = get_last_messages()

        for message in history:
            await websocket.send(f"HISTORIA: {message}")

        async for message in websocket:
            save_message(message)

            for client in clients:
                await client.send(message)

    finally:
        clients.remove(websocket)


async def main():
    init_db()

    async with websockets.serve(handler, "localhost", 8765):
        print("Serwer WebSocket działa na ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())
