from celery import shared_task
from datetime import datetime


@shared_task
def hello_world():
    print("Hello from Celery!")


@shared_task
def multiply(a, b):
    return a * b


@shared_task
def log_timestamp():
    with open("log.txt", "a") as file:
        file.write(f"{datetime.now()}\n")


@shared_task
def count_users():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    count = User.objects.count()

    print(f"Liczba użytkowników w bazie danych: {count}")

    return count
