import json

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from blog.models import Category


class Command(BaseCommand):
    help = "Seed blog categories"

    def handle(self, *args, **options):
        with open("blog/seed_data/categories.json", encoding="utf-8") as file:
            categories = json.load(file)

        self.create_categories(categories)

        self.stdout.write(
            self.style.SUCCESS("Categories seeded successfully.")
        )

    def create_categories(self, categories, parent=None):
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data["name"],
                parent=parent,
                defaults={
                    "slug": slugify(category_data["name"]),
                },
            )

            if created:
                self.stdout.write(
                    f"Created: {category.name}"
                )

            children = category_data.get("children", [])

            self.create_categories(
                children,
                parent=category,
            )