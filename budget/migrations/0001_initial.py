# Generated by Django 5.0.6 on 2024-06-10 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Budget",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.UUIDField()),
                ("amount", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
