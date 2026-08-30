import graphene


users = []


class User(graphene.ObjectType):
    name = graphene.String()
    email = graphene.String()


class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(root, info):
        return users


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(User)

    def mutate(root, info, name, email):
        user = {"name": name, "email": email}
        users.append(user)
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

mutation = """
mutation {
    createUser(name: "Jan", email: "jan@example.com") {
        user {
            name
            email
        }
    }
}
"""

result = schema.execute(mutation)

print(result.data)
print(result.errors)
