import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


users = [
    User(id="1", name="Jan Kowalski", email="jan@example.com"),
    User(id="2", name="Anna Nowak", email="anna@example.com"),
]


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User | None:
        for user in users:
            if user.id == id:
                return user
        return None


schema = strawberry.Schema(query=Query)

app = web.Application()
app.router.add_route(
    "*",
    "/graphql",
    GraphQLView(schema=schema),
)


if __name__ == "__main__":
    web.run_app(app, host="localhost", port=8080)
