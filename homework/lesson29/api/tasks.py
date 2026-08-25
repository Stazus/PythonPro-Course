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


@shared_task(bind=True)
def progress_task(self):
    import time

    for i in range(1, 101):
        time.sleep(0.1)

        self.update_state(
            state="PROGRESS",
            meta={
                "current": i,
                "total": 100,
            },
        )

    return {
        "current": 100,
        "total": 100,
        "status": "Zakończono",
    }


@shared_task
def cleanup_old_logs():
    from datetime import timedelta

    from django.utils import timezone

    from .models import LogEntry

    cutoff_date = timezone.now() - timedelta(days=90)

    deleted_count, _ = LogEntry.objects.filter(
        created_at__lt=cutoff_date
    ).delete()

    print(f"Usunięto starych wpisów logów: {deleted_count}")

    return deleted_count


@shared_task
def scrape_example_title():
    import requests
    from bs4 import BeautifulSoup

    from .models import ScrapedPage

    url = "https://example.com"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip()

    scraped_page = ScrapedPage.objects.create(
        url=url,
        title=title,
    )

    print(f"Pobrano tytuł strony: {title}")

    return scraped_page.id


@shared_task
def generate_users_csv():
    import csv
    from pathlib import Path

    from django.conf import settings
    from django.contrib.auth import get_user_model

    User = get_user_model()

    reports_dir = Path(settings.MEDIA_ROOT) / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    file_path = reports_dir / "users.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["username", "email"])

        for user in User.objects.all():
            writer.writerow([user.username, user.email])

    return "reports/users.csv"


@shared_task(bind=True)
def retry_failed_request(self):
    import requests

    url = "https://this-address-does-not-exist.invalid"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return {
            "status": "success",
            "status_code": response.status_code,
        }

    except requests.RequestException as exc:
        print(
            f"Błąd połączenia. "
            f"Próba {self.request.retries + 1}. "
            f"Ponowienie za 60 sekund."
        )

        raise self.retry(
            exc=exc,
            countdown=60,
            max_retries=3,
        )


@shared_task
def classify_uploaded_image(image_id):
    from PIL import Image

    from .models import UploadedImage

    uploaded_image = UploadedImage.objects.get(id=image_id)

    with Image.open(uploaded_image.image.path) as image:
        mode = image.mode
        width, height = image.size

        if mode == "L":
            image_type = "skala szarości"
        else:
            image_type = "obraz kolorowy"

        result = (
            f"Typ: {image_type}; "
            f"tryb: {mode}; "
            f"wymiary: {width}x{height}"
        )

    uploaded_image.classification_result = result
    uploaded_image.save(update_fields=["classification_result"])

    print(f"Klasyfikacja obrazu {image_id}: {result}")

    return result


@shared_task
def generate_random_number():
    import random

    number = random.randint(1, 100)

    print(f"Wylosowano liczbę: {number}")

    return number


@shared_task
def multiply_by_ten(number):
    result = number * 10

    print(f"{number} * 10 = {result}")

    return result


@shared_task
def save_chain_result(result):
    from pathlib import Path

    from django.conf import settings

    results_dir = Path(settings.MEDIA_ROOT) / "chain_results"
    results_dir.mkdir(parents=True, exist_ok=True)

    file_path = results_dir / "result.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Wynik łańcucha zadań: {result}\n")

    print(f"Zapisano wynik do pliku: {result}")

    return "chain_results/result.txt"


@shared_task
def send_priority_email():
    from django.core.mail import send_mail

    send_mail(
        subject="Wiadomość priorytetowa",
        message="To jest wiadomość wysłana przez priority_queue.",
        from_email="noreply@example.com",
        recipient_list=["test@example.com"],
        fail_silently=False,
    )

    print("Wysłano wiadomość z kolejki priorytetowej.")

    return "Wiadomość priorytetowa została wysłana."
