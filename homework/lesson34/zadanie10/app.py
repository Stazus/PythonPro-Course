import graphene


users_data = [
    {"id": 1, "name": "Jan"},
    {"id": 2, "name": "Anna"},
]

posts_data = [
    {"id": 1, "title": "Pierwszy post", "author_id": 1},
    {"id": 2, "title": "Drugi post", "author_id": 1},
    {"id": 3, "title": "Post Anny", "author_id": 2},
]


class Post(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    author = graphene.Field(lambda: User)

    def resolve_author(parent, info):
        return next(
            user for user in users_data
            if user["id"] == parent["author_id"]
        )


class User(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    posts = graphene.List(Post)

    def resolve_posts(parent, info):
        return [
            post for post in posts_data
            if post["author_id"] == parent["id"]
        ]


class Query(graphene.ObjectType):
    users = graphene.List(User)
    posts = graphene.List(Post)

    def resolve_users(root, info):
        return users_data

    def resolve_posts(root, info):
        return posts_data


schema = graphene.Schema(query=Query)


query = """
{
    users {
        name
        posts {
            title
            author {
                name
            }
        }
    }
}
"""

result = schema.execute(query)

print(result.data)
print(result.errors)
