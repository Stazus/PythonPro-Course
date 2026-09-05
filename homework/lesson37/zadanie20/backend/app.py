import json
import os

import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from celery_app import celery_app
from tasks import (
    create_recommendations,
    recommendation_cache_key,
)


app = FastAPI(
    title="AI Book Recommendation API"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://appuser:apppassword@database:5432/booksdb",
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/2",
)

engine = create_engine(DATABASE_URL)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


class RecommendationRequest(BaseModel):
    preferences: str


@app.get("/")
def root():
    return {
        "message": "AI Book Recommendation API działa"
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        redis_client.ping()

        return {
            "status": "ok",
            "postgresql": "ok",
            "redis": "ok",
        }

    except (
        SQLAlchemyError,
        redis.RedisError,
    ) as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )


@app.post("/recommend")
def recommend(
    request: RecommendationRequest,
):
    preferences = request.preferences.strip()

    if not preferences:
        raise HTTPException(
            status_code=400,
            detail="Preferencje nie mogą być puste.",
        )

    cache_key = recommendation_cache_key(
        preferences
    )

    cached_result = redis_client.get(
        cache_key
    )

    if cached_result:
        return {
            "cached": True,
            "recommendations": json.loads(
                cached_result
            ),
        }

    task = create_recommendations.delay(
        preferences
    )

    return {
        "cached": False,
        "task_id": task.id,
    }


@app.get("/result/{task_id}")
def result(task_id: str):
    task = celery_app.AsyncResult(task_id)

    if not task.ready():
        return {
            "status": task.status,
            "recommendations": None,
        }

    if task.failed():
        return {
            "status": "FAILURE",
            "error": str(task.result),
        }

    return {
        "status": "SUCCESS",
        "recommendations": task.result,
    }


@app.get("/history")
def history():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT
                        id,
                        preferences,
                        recommendations,
                        created_at
                    FROM recommendation_history
                    ORDER BY created_at DESC
                    LIMIT 20
                    """
                )
            )

            rows = result.mappings().all()

        return [
            {
                "id": row["id"],
                "preferences": row["preferences"],
                "recommendations": json.loads(
                    row["recommendations"]
                ),
                "created_at": row[
                    "created_at"
                ],
            }
            for row in rows
        ]

    except SQLAlchemyError:
        return []
