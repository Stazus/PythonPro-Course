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
