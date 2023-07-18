from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=200,
        unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(
        verbose_name='Автор',
        max_length=300,
        unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(verbose_name='Название', max_length=150)
    author = models.ForeignKey(
        Author,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='books')
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        null=True,
        # книги останутся в БД при удалении жанра:
        on_delete=models.SET_NULL,
        related_name='books')
    year = models.SmallIntegerField(
        verbose_name='Год издания',
        validators=[
            MinValueValidator(0), MaxValueValidator(datetime.now().year)],
        blank=True,
        null=True)
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True)
    cover = models.ImageField(
        verbose_name='Обложка',
        upload_to='books/',
        blank=True,
        null=True)
    added_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True)

    @property
    def rating(self):
        rating = (Review.objects.filter(book=self).
                  aggregate(Avg('score')).get('score__avg'))
        if rating is None:
            return 'отсутствует'
        else:
            return rating

    class Meta:
        ordering = ('added_date',)

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name='Книга',
        # отзыв удалится при удалении книги:
        on_delete=models.CASCADE,
        related_name='reviews')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        null=True,
        # отзыв останется в БД при удалении автора:
        on_delete=models.SET_NULL,
        related_name='reviews')
    text = models.TextField(
        verbose_name='Текст отзыва',
        blank=True,
        null=True)
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка (от 1 до 10)',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False)
    added_date = models.DateTimeField(
        verbose_name='Дата добавления отзыва',
        auto_now_add=True)
    edited_date = models.DateTimeField(
        verbose_name='Дата редактирования отзыва',
        auto_now=True)

    class Meta:
        unique_together = ['author', 'book']
        ordering = ('-added_date',)

    def __str__(self):
        return f'{self.book} ({self.score})'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    added_date = models.DateTimeField(
        verbose_name='Дата добавления комментария',
        auto_now_add=True)
    edited_date = models.DateTimeField(
        verbose_name='Дата редактирования комментария',
        auto_now=True)

    class Meta:
        ordering = ('added_date',)

    def __str__(self):
        return self.text


class BookRead(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name='Книга',
        on_delete=models.CASCADE,
        related_name='books_read')
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='books_read')
    added_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ('added_date',)

    def __str__(self):
        return f'{self.user.username} - {self.book.name}'


class BookToRead(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name='Книга',
        on_delete=models.CASCADE,
        related_name='books_to_read')
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='books_to_read')
    added_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ('added_date',)

    def __str__(self):
        return f'{self.user.username} - {self.book.name}'


# class Recommendation(models.Model):
#     book = models.ForeignKey(
#         Book,
#         verbose='Книга',
#         on_delete=models.CASCADE,
#         related_name='recommendations')
#     user = models.ForeignKey(
#         User,
#         verbose_name='Пользователь',
#         on_delete=models.CASCADE,
#         related_name='recommendations')
#     added_date = models.DateTimeField(
#         verbose_name='Дата добавления',
#         auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'book']
#         ordering = ('added_date',)

#     def __str__(self):
#         return f'{self.user.username} - {self.book.name}'
