from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from core.utils import get_paginator

from .models import Genre, Author, Book, Review, Comment, BookRead, BookToRead


def home(request):
    return render(request, 'books/home.html')


def books(request):
    book_list = Book.objects.all()
    context = {
        'page_obj': get_paginator(request, book_list)
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


def search_books(request):
    return HttpResponse('Поиск книг')
