# Generated by Django 4.2.2 on 2023-07-29 18:55

import datetime

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 7, 30))], verbose_name='Дата рождения'),
        ),
    ]
