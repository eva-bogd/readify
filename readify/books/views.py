from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from core.utils import get_paginator

from .models import Genre, Author, Book, Review, Comment, BookRead, BookToRead

User = get_user_model()


def home(request):
    return render(request, 'books/home.html')


def books(request):
    book_list = Book.objects.all()
    context = {
        'page_obj': get_paginator(request, book_list),
    }
    return render(request, 'books/books.html', context)


def books_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'books/books_detail.html', context)


def books_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    book_list = genre.books.all()
    context = {
        'genre': genre,
        'page_obj': get_paginator(request, book_list)
    }
    return render(request, 'books/books_genre.html', context)


def author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    author_list = author.books.all()
    context = {
        'author': author,
        'page_obj': get_paginator(request, author_list)
    }
    return render(request, 'books/author.html', context)


# Прочитанные книги
@login_required
def book_read(request):
    book_list = Book.objects.filter(books_read__user=request.user)
    context = {
        'page_obj': get_paginator(request, book_list),
    }
    return render(request, 'books/book_read.html', context)


@login_required
def add_book_read(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    if not BookRead.objects.filter(user=user, book=book).exists():
        BookRead.objects.create(user=user, book=book)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_book_read(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    get_object_or_404(BookRead, user=user, book=book).delete()
    return redirect(request.META.get('HTTP_REFERER'))


# Запланированные книги
@login_required
def book_to_read(request):
    book_list = Book.objects.filter(books_to_read__user=request.user)
    context = {
         'page_obj': get_paginator(request, book_list)
    }
    return render(request, 'books/book_to_read.html', context)


@login_required
def add_book_to_read(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    if not BookToRead.objects.filter(user=user, book=book).exists():
        BookToRead.objects.create(user=user, book=book)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_book_to_read(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    get_object_or_404(BookToRead, user=user, book=book).delete()
    return redirect(request.META.get('HTTP_REFERER'))


def search_books(request):
    return HttpResponse('Поиск книг')
