import asyncio
from collections import defaultdict

import strawberry
from strawberry.dataloader import DataLoader


users_data = [
    {"id": 1, "name": "Jan"},
    {"id": 2, "name": "Anna"},
    {"id": 3, "name": "Piotr"},
]

posts_data = [
    {"id": 1, "title": "Post Jana 1", "author_id": 1},
    {"id": 2, "title": "Post Jana 2", "author_id": 1},
    {"id": 3, "title": "Post Anny", "author_id": 2},
    {"id": 4, "title": "Post Piotra", "author_id": 3},
]


async def load_posts_for_users(user_ids):
    print(f"Jedno zbiorcze pobranie postów dla użytkowników: {user_ids}")

    posts_by_user = defaultdict(list)

    for post in posts_data:
        if post["author_id"] in user_ids:
            posts_by_user[post["author_id"]].append(post)

    return [posts_by_user[user_id] for user_id in user_ids]


post_loader = DataLoader(load_fn=load_posts_for_users)


@strawberry.type
class Post:
    id: int
    title: str


@strawberry.type
class User:
    id: int
    name: str

    @strawberry.field
    async def posts(self) -> list[Post]:
        posts = await post_loader.load(self.id)

        return [
            Post(
                id=post["id"],
                title=post["title"],
            )
            for post in posts
        ]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [
            User(
                id=user["id"],
                name=user["name"],
            )
            for user in users_data
        ]


schema = strawberry.Schema(query=Query)


async def main():
    query = """
    {
        users {
            id
            name
            posts {
                id
                title
            }
        }
    }
    """

    result = await schema.execute(query)

    print(result.data)
    print("Błędy:", result.errors)


asyncio.run(main())
