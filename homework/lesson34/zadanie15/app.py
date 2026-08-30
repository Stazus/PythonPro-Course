import asyncio
from typing import AsyncGenerator

import strawberry
from strawberry.asgi import GraphQL


users = []
subscribers = []


@strawberry.type
class User:
    name: str
    email: str


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return users


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        users.append(user)

        for queue in subscribers:
            await queue.put(user)

        return user


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self) -> AsyncGenerator[User, None]:
        queue = asyncio.Queue()
        subscribers.append(queue)

        try:
            while True:
                user = await queue.get()
                yield user
        finally:
            subscribers.remove(queue)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)

app = GraphQL(schema)
