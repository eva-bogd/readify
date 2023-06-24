# Generated by Django 4.2.2 on 2023-06-22 19:01

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 6, 23))], verbose_name='Дата рождения'),
        ),
    ]
