import random

from django.core.management.base import BaseCommand

from api.tasks import multiply


class Command(BaseCommand):
    help = "Dodaje do kolejki Celery 50 zadań multiply z losowymi argumentami."

    def handle(self, *args, **options):
        for i in range(50):
            a = random.randint(1, 100)
            b = random.randint(1, 100)

            task = multiply.delay(a, b)

            self.stdout.write(
                f"Zadanie {i + 1}: {a} * {b}, task_id={task.id}"
            )

        self.stdout.write(
            self.style.SUCCESS("Dodano 50 zadań multiply do kolejki Celery.")
        )
