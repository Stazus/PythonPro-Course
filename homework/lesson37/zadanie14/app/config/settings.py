import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "zadanie14-secret-key"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "tasks",
]

MIDDLEWARE = []

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "taskdb"),
        "USER": os.getenv("POSTGRES_USER", "taskuser"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "taskpassword"),
        "HOST": os.getenv("POSTGRES_HOST", "database"),
        "PORT": "5432",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
