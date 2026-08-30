from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import engine, get_db
from models import Base, Comment, Post, User
from schemas import (
    CommentCreate,
    CommentResponse,
    PostCreate,
    PostResponse,
    PostWithCommentsResponse,
    UserCreate,
    UserResponse,
)


app = FastAPI(title="Blog API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def send_comment_email(post_id: int):
    with open("emails.log", "a", encoding="utf-8") as file:
        file.write(
            f"Email sent: new comment added to post {post_id}.\n"
        )

def generate_summary(content: str) -> str:
    if len(content) <= 120:
        return content

    return content[:120] + "..."


def analyze_comment_sentiment(
    comment_id: int,
    content: str,
):
    text = content.lower()

    positive_words = {
        "dobry",
        "super",
        "świetny",
        "swietny",
        "lubię",
        "lubie",
        "polecam",
    }

    negative_words = {
        "zły",
        "zly",
        "słaby",
        "slaby",
        "fatalny",
        "beznadziejny",
    }

    sentiment = "neutral"

    if any(word in text for word in positive_words):
        sentiment = "positive"

    if any(word in text for word in negative_words):
        sentiment = "negative"

    with open(
        "sentiment.log",
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            f"comment_id={comment_id} "
            f"sentiment={sentiment}\n"
        )

BANNED_WORDS = {
    "kurwa",
    "chuj",
    "pierdol",
}


@app.middleware("http")
async def content_moderation_middleware(
    request: Request,
    call_next,
):
    if request.method in {"POST", "PUT", "PATCH"}:
        body = await request.body()

        if body:
            text = body.decode("utf-8").lower()

            if any(word in text for word in BANNED_WORDS):
                return JSONResponse(
                    status_code=400,
                    content={
                        "detail": "Content contains forbidden words"
                    },
                )

    response = await call_next(request)
    return response


# USERS CRUD

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    new_user = User(
        name=user.name,
        email=user.email,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@app.get(
    "/users",
    response_model=list[UserResponse],
)
async def get_users(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User))
    return result.scalars().all()


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.name = user_data.name
    user.email = user_data.email

    await db.commit()
    await db.refresh(user)

    return user


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    await db.delete(user)
    await db.commit()


# POSTS CRUD

@app.post(
    "/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
):
    author = await db.get(User, post.author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=post.author_id,
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


@app.get(
    "/posts",
    response_model=list[PostResponse],
)
async def get_posts(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post))
    return result.scalars().all()


@app.get(
    "/posts/{post_id}",
    response_model=PostResponse,
)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    post = await db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return post


@app.put(
    "/posts/{post_id}",
    response_model=PostResponse,
)
async def update_post(
    post_id: int,
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
):
    post = await db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.author_id != post_data.author_id:
        raise HTTPException(
            status_code=403,
            detail="Only author can edit this post",
        )

    post.title = post_data.title
    post.content = post_data.content

    await db.commit()
    await db.refresh(post)

    return post


@app.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    post = await db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    await db.delete(post)
    await db.commit()


# COMMENTS

@app.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    post = await db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    new_comment = Comment(
        content=comment.content,
        post_id=post_id,
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    background_tasks.add_task(
        send_comment_email,
        post_id,
    )

    background_tasks.add_task(
        analyze_comment_sentiment,
        new_comment.id,
        new_comment.content,
    )

    return new_comment


@app.post("/posts/{post_id}/summarize")
async def summarize_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    post = await db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    summary = generate_summary(post.content)

    return {
        "post_id": post.id,
        "summary": summary,
    }


# POST WITH COMMENTS - EAGER LOADING

@app.get(
    "/posts/{post_id}/with-comments",
    response_model=PostWithCommentsResponse,
)
async def get_post_with_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.comments))
        .where(Post.id == post_id)
    )

    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return post
