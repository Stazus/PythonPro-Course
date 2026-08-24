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


@shared_task
def update_user_last_login(user_id):
    from django.contrib.auth import get_user_model
    from django.utils import timezone

    User = get_user_model()
    user = User.objects.get(id=user_id)

    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])

    return user.id


@shared_task
def process_video():
    import time

    time.sleep(15)

    print("Przetwarzanie wideo zakończone!")

    return "Przetwarzanie wideo zakończone!"


@shared_task
def send_email_notification(notification_id):
    from django.utils import timezone
    from .models import EmailNotification

    notification = EmailNotification.objects.get(id=notification_id)

    print(
        f"Wysyłka maila do: {notification.recipient_email} | "
        f"Temat: {notification.subject}"
    )

    notification.sent_at = timezone.now()
    notification.save(update_fields=["sent_at"])

    return notification.id
