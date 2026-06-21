from django.core.management.base import BaseCommand
from faker import Faker
import random

from notatnik.models import Category, Post


class Command(BaseCommand):
    help = "Tworzy przykładowe kategorie i 100 postów"

    def handle(self, *args, **kwargs):
        fake = Faker("pl_PL")

        Post.objects.all().delete()
        Category.objects.all().delete()

        category_names = [
            "Technologia",
            "Podróże",
            "Kulinaria",
            "Sport",
            "Python",
            "Django",
            "Finanse",
        ]

        categories = []

        for name in category_names:
            category = Category.objects.create(name=name)
            categories.append(category)

        for _ in range(100):
            Post.objects.create(
                title=fake.sentence(nb_words=4),
                content=fake.text(),
                category=random.choice(categories),
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Utworzono 100 postów i kategorie."
            )
        )
