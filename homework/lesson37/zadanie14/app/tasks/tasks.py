import time

from celery import shared_task


@shared_task
def process_task(message):
    print(f"Rozpoczynam zadanie: {message}")

    time.sleep(5)

    result = f"Zadanie zakończone: {message}"
    print(result)

    return result
