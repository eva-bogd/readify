# Generated by Django 4.2.2 on 2023-06-22 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookread',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookreads', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
