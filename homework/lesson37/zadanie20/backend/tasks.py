import hashlib
import json
import math
import os

import redis
import requests
from sqlalchemy import create_engine, text

from celery_app import celery_app


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://appuser:apppassword@database:5432/booksdb",
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/2",
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434",
)


BOOKS = [
    {
        "title": "Diuna",
        "author": "Frank Herbert",
        "description": (
            "Epicka powieść science fiction o polityce, ekologii, "
            "pustynnej planecie i walce o władzę."
        ),
    },
    {
        "title": "Fundacja",
        "author": "Isaac Asimov",
        "description": (
            "Science fiction o przyszłości galaktycznej cywilizacji, "
            "nauce, historii i przewidywaniu losów społeczeństw."
        ),
    },
    {
        "title": "Wiedźmin: Ostatnie życzenie",
        "author": "Andrzej Sapkowski",
        "description": (
            "Fantasy o łowcy potworów, magii, moralnych wyborach "
            "i słowiańskich motywach."
        ),
    },
    {
        "title": "Złodziejka książek",
        "author": "Markus Zusak",
        "description": (
            "Powieść historyczna osadzona podczas II wojny światowej "
            "o książkach, przyjaźni i dorastaniu."
        ),
    },
    {
        "title": "Projekt Hail Mary",
        "author": "Andy Weir",
        "description": (
            "Science fiction o samotnej misji kosmicznej, nauce, "
            "zagadkach i próbie uratowania ludzkości."
        ),
    },
    {
        "title": "Imię róży",
        "author": "Umberto Eco",
        "description": (
            "Historyczna powieść detektywistyczna o tajemniczych "
            "morderstwach w średniowiecznym klasztorze."
        ),
    },
]


def recommendation_cache_key(preferences: str) -> str:
    normalized = preferences.strip().lower()

    digest = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()

    return f"recommendations:{digest}"


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    norm_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    norm_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def create_embedding(text_to_embed: str):
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text_to_embed,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["embedding"]


@celery_app.task
def create_recommendations(preferences: str):
    user_embedding = create_embedding(
        preferences
    )

    recommendations = []

    for book in BOOKS:
        book_embedding = create_embedding(
            book["description"]
        )

        score = cosine_similarity(
            user_embedding,
            book_embedding,
        )

        recommendations.append(
            {
                "title": book["title"],
                "author": book["author"],
                "score": round(score, 4),
            }
        )

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    top_recommendations = recommendations[:3]

    redis_client = redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True,
    )

    redis_client.setex(
        recommendation_cache_key(preferences),
        3600,
        json.dumps(
            top_recommendations,
            ensure_ascii=False,
        ),
    )

    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS recommendation_history (
                    id SERIAL PRIMARY KEY,
                    preferences TEXT NOT NULL,
                    recommendations TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )
        )

        connection.execute(
            text(
                """
                INSERT INTO recommendation_history (
                    preferences,
                    recommendations
                )
                VALUES (
                    :preferences,
                    :recommendations
                )
                """
            ),
            {
                "preferences": preferences,
                "recommendations": json.dumps(
                    top_recommendations,
                    ensure_ascii=False,
                ),
            },
        )

    return top_recommendations
