# Generated by Django 4.2.2 on 2023-07-12 06:12

import datetime

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 7, 12))], verbose_name='Дата рождения'),
        ),
    ]
