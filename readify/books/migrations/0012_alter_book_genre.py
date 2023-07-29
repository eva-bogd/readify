# Generated by Django 4.2.2 on 2023-07-29 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_book_options_alter_review_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='books', to='books.genre', verbose_name='Жанр'),
        ),
    ]
