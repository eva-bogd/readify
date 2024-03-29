# Generated by Django 4.2.2 on 2023-07-12 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='edited_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата редактирования комментария'),
        ),
        migrations.AddField(
            model_name='review',
            name='edited_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата редактирования отзыва'),
        ),
    ]
