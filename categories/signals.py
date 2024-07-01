from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category


@receiver(post_migrate)
def populate_categories(sender, **kwargs):
    if sender.name == "categories":
        categories = [
            {"id": 1, "name": "Comida"},
            {"id": 2, "name": "Vivienda"},
            {"id": 3, "name": "Educación"},
            {"id": 4, "name": "Salud"},
            {"id": 5, "name": "Entretenimiento"},
            {"id": 6, "name": "Ahorro"},
            {"id": 7, "name": "Inversión"},
            {"id": 8, "name": "Transporte"},
        ]
        for category in categories:
            Category.objects.get_or_create(id=category["id"], defaults=category)
