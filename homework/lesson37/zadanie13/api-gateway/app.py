from fastapi import FastAPI
import httpx

app = FastAPI()


@app.get("/feed")
async def get_feed():
    async with httpx.AsyncClient() as client:
        users_response = await client.get("http://users-service:8000/users")
        posts_response = await client.get("http://posts-service:8000/posts")

    users = users_response.json()
    posts = posts_response.json()

    users_by_id = {user["id"]: user["name"] for user in users}

    result = []

    for post in posts:
        result.append(
            {
                "post_id": post["id"],
                "title": post["title"],
                "user_id": post["user_id"],
                "user_name": users_by_id.get(post["user_id"], "Nieznany użytkownik"),
            }
        )

    return result
