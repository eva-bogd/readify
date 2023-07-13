from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages

from core.utils import get_paginator

from .models import Genre, Author, Book, Review, Comment, BookRead, BookToRead
from .forms import ReviewForm, CommentForm, SearchForm

User = get_user_model()


def home(request):
    return render(request, 'books/home.html')


def books(request):
    book_list = Book.objects.all()
    context = {
        'page_obj': get_paginator(request, book_list)
    }
    return render(request, 'books/books.html', context)


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


def books_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    review_form = ReviewForm()
    reviews = book.reviews.all()
    comments = Comment.objects.filter(review__in=reviews)
    context = {
        'book': book,
        'review_form': review_form,
        'reviews': reviews,
        'comments': comments
    }
    return render(request, 'books/books_detail.html', context)


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    review_form = ReviewForm(request.POST or None)
    reviews = book.reviews.all()
    comments = Comment.objects.filter(review__in=reviews)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.book = book
        review.author = request.user
        try:
            review.save()
            return redirect('books:books_detail', book_id=book_id)
        except IntegrityError:
            messages.error(request, "Вы уже оставили отзыв на эту книгу.")
    context = {
        'book': book,
        'review_form': review_form,
        'reviews': reviews,
        'comments': comments
    }
    # else:
    #     messages.error(request, "Неверный формат отзыва.")
    #     review_form.add_error(None, "Ошибка добавления отзыва")
    # return redirect('books:books_detail', book_id=book_id)
    return render(request, 'books/books_detail.html', context)


@login_required
def edit_review(request, book_id, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,  # author=request.user)
        book_id=book_id)
    if request.user != review.author:
        return redirect('books:books_detail', book_id=book_id)
    review_form = ReviewForm(request.POST or None, instance=review)
    if review_form.is_valid():
        review = review_form.save()
        return redirect('books:books_detail', book_id=book_id)
    context = {
        'book_id': book_id,
        'review_id': review_id,
        'review_form': review_form,
    }
    return render(request, 'books/edit_review.html', context)


@login_required
def add_comment(request, book_id, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        book_id=book_id)
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.review = review
        comment.save()
        return redirect('books:books_detail', book_id=book_id)
    context = {
        'book_id': book_id,
        'review_id': review_id,
        'comment_form': comment_form,
    }
    return render(request, 'books/add_comment.html', context)


@login_required
def edit_comment(request, book_id, review_id, comment_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        book_id=book_id)
    comment = get_object_or_404(
        Comment,
        id=comment_id,  # author=request.user)
        review=review)
    if request.user != comment.author:
        return redirect('books:books_detail', book_id=book_id)
    comment_form = CommentForm(request.POST or None, instance=comment)
    if comment_form.is_valid():
        comment.save()
        return redirect('books:books_detail', book_id=book_id)
    context = {
        'book_id': book_id,
        'review_id': review_id,
        'comment_id': comment_id,
        'comment_form': comment_form,
    }
    return render(request, 'books/edit_comment.html', context)


# Прочитанные книги
@login_required
def book_read(request):
    book_list = Book.objects.filter(books_read__user=request.user)
    context = {
        'page_obj': get_paginator(request, book_list)
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
    search_query = request.GET.get('query', '')
    book_list = []
    if search_query:
        book_list = Book.objects.filter(
            Q(name__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(genre__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    search_form = SearchForm(request.GET or None)
    context = {
        'book_list': book_list,
        'search_form': search_form,
    }
    return render(request, 'books/search_books.html', context)
