from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books')
    genre = models.ForeignKey(
        Genre,
        null=True,
        # книги останутся в БД при удалении жанра:
        on_delete=models.SET_NULL,
        related_name='books')
    year = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), MaxValueValidator(datetime.now().year)],
        blank=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='books/', blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    @property
    def rating(self):
        rating = (Review.objects.filter(book=self).
                  aggregate(Avg('score')).get('score__avg'))
        if rating is None:
            return None
        else:
            return round(rating)

    class Meta:
        ordering = ('-added_date',)

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        # отзыв удалится при удалении книги:
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        null=True,
        # отзыв останется в БД при удалении автора:
        on_delete=models.SET_NULL,
        related_name='reviews')
    text = models.TextField(blank=True)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['author', 'book']
        ordering = ('-added_date',)

    def __str__(self):
        return f'{self.book} ({self.score})'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField(blank=False)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-added_date',)

    def __str__(self):
        return self.text


class BookRead(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='books_read'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books_read'
    )
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ('added_date',)

    def __str__(self):
        return f'{self.user.username} - {self.book.name}'


class BookToRead(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='books_to_read'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books_to_read'
    )
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ('added_date',)

    def __str__(self):
        return f'{self.user.username} - {self.book.name}'
