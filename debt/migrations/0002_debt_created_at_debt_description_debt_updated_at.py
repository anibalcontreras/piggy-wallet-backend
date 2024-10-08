# Generated by Django 5.0.6 on 2024-07-01 19:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("debt", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="debt",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="debt",
            name="description",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="debt",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
