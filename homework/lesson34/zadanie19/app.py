import asyncio
from typing import AsyncGenerator

import strawberry
from strawberry.asgi import GraphQL


users = [
    {"id": 1, "name": "Jan"},
    {"id": 2, "name": "Anna"},
]

messages = []
subscribers = []


@strawberry.type
class User:
    id: int
    name: str


@strawberry.type
class Message:
    user: str
    text: str


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [
            User(id=user["id"], name=user["name"])
            for user in users
        ]

    @strawberry.field
    def chat_history(self) -> list[Message]:
        return messages


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def send_message(self, user: str, text: str) -> Message:
        message = Message(user=user, text=text)
        messages.append(message)

        for queue in subscribers:
            await queue.put(message)

        return message


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def new_message(self) -> AsyncGenerator[Message, None]:
        queue = asyncio.Queue()
        subscribers.append(queue)

        try:
            while True:
                message = await queue.get()
                yield message
        finally:
            subscribers.remove(queue)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)

app = GraphQL(schema)
