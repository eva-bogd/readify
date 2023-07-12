# Generated by Django 4.2.2 on 2023-07-12 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_comment_edited_date_alter_review_edited_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='edited_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата редактирования комментария'),
        ),
        migrations.AlterField(
            model_name='review',
            name='edited_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата редактирования отзыва'),
        ),
    ]
