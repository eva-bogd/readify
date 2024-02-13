[![Built with Django](https://img.shields.io/badge/Built_with-Django-32CD32.svg)](https://www.djangoproject.com/)
[![Built with Django REST framework](https://img.shields.io/badge/Built_with-Django_REST_framework-green.svg)](https://www.django-rest-framework.org/)

## Readify

**Readify** - пет-проект для поиска и обсуждения книг. Пользователь может создать профиль на сайте, добавлять книги в список прочитанных или запланированных книг, получать рекомендации, оценивать книги, оставлять отзывы и комментарии. Проект содержит REST API.

**Проект доступен по адресу https://finny.pythonanywhere.com/**

### Как локально запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Eva-48k/readify.git
```

```
cd readify
```

2. Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
venv/scripts/activate
```

3. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

5. Запустить проект:

```
python manage.py runserver
```
