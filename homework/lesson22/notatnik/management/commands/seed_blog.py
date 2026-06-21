from django.core.management.base import BaseCommand
from faker import Faker
import random

from notatnik.models import Category, Post, Tag


class Command(BaseCommand):
    help = "Tworzy przykładowe kategorie, tagi i 100 postów"

    def handle(self, *args, **kwargs):
        fake = Faker("pl_PL")

        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

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

        tag_names = [
            "Python",
            "Django",
            "Web",
            "Baza danych",
            "Podróże",
            "Jedzenie",
            "Sport",
            "Finanse",
            "Technologia",
            "Porady",
        ]

        tags = []

        for name in tag_names:
            tag = Tag.objects.create(name=name)
            tags.append(tag)

        for _ in range(100):
            post = Post.objects.create(
                title=fake.sentence(nb_words=4),
                content=fake.text(),
                category=random.choice(categories),
            )

            random_tags = random.sample(
                tags,
                random.randint(1, 5)
            )

            post.tags.set(random_tags)

        self.stdout.write(
            self.style.SUCCESS(
                "Utworzono 100 postów, kategorie i tagi."
            )
        )
