# Generated by Django 5.2.2 on 2025-06-24 13:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_seed_iconic'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='critica',
            name='liked_users',
            field=models.ManyToManyField(blank=True, related_name='liked_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
