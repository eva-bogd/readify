from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский')
    ]
    birth_date = models.DateField(
        validators=[MaxValueValidator(datetime.now().date())],
        verbose_name='Дата рождения',
        blank=True,
        null=True)
    gender = models.CharField(
        verbose_name='Пол',
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='users/',
        blank=True,
        null=True)
    show_book_read = models.BooleanField(
        verbose_name='Показывать другим пользователям мои прочитанные книги',
        default=True)
    show_book_to_read = models.BooleanField(
        verbose_name='Показывать другим пользователям мои запланированные книги',
        default=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
