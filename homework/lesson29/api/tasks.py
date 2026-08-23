from celery import shared_task


@shared_task
def hello_world():
    print("Hello from Celery!")


@shared_task
def multiply(a, b):
    return a * b
