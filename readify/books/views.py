from urllib.parse import quote_plus

from core.utils import get_paginator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template

from .forms import CommentForm, FeedbackForm, ReviewForm, SearchForm
from .models import Author, Book, BookRead, BookToRead, Comment, Genre, Review
from .services import BookRecommendationService

User = get_user_model()


def home(request):
    book_list = Book.objects.all().order_by('-added_date')[:10]
    context = {
        'page_obj': get_paginator(request, book_list)
    }
    return render(request, 'books/home.html', context)


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


def book_author(request, author_id):
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
    reviews = book.reviews.all().prefetch_related('comments')
    # для URL-кодирования строки
    search_query = quote_plus(book.name)  # заменяет пробелы на '+'
    search_url = f"https://www.litres.ru/search/?q={search_query}"
    context = {
        'book': book,
        'review_form': review_form,
        'reviews': reviews,
        'search_url': search_url
    }
    return render(request, 'books/books_detail.html', context)


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    review_form = ReviewForm(request.POST or None)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.book = book
        review.author = request.user
        try:
            review.save()
            return redirect('books:books_detail', book_id=book_id)
        except IntegrityError:
            messages.error(request, "Вы уже оставили отзыв на эту книгу.")
    reviews = book.reviews.all().prefetch_related('comments')
    context = {
        'book': book,
        'review_form': review_form,
        'reviews': reviews,
    }
    return render(request, 'books/books_detail.html', context)


@login_required
def edit_review(request, book_id, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
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
        id=comment_id,
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


def book_read(request, user_id):
    user = request.user
    owner = get_object_or_404(User, id=user_id)
    if user.id != owner.id and owner.show_book_read is False:
        return HttpResponse("Список прочитанных книг недоступен", status=403)
    book_list = Book.objects.filter(books_read__user_id=user_id)
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


def book_to_read(request, user_id):
    user = request.user
    owner = get_object_or_404(User, id=user_id)
    if user.id != owner.id and owner.show_book_to_read is False:
        return HttpResponse("Список прочитанных книг недоступен", status=403)
    book_list = Book.objects.filter(books_to_read__user_id=user_id)
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


@login_required
def recommendations(request):
    user = request.user
    book_list = BookRecommendationService.get_recommendations_for_user(
            user_id=user.id)
    context = {
        'page_obj': get_paginator(request, book_list),
    }
    return render(request, 'books/recommendations.html', context)


def search_books(request):
    # '' - пустая строка дефолтое значение
    search_query = request.GET.get('search', '')
    book_list = []
    if search_query:
        keywords = search_query.split()
        query = Q()
        for keyword in keywords:
            query |= (  # для объединения условий
                      Q(name__icontains=keyword) |
                      Q(author__name__icontains=keyword) |
                      Q(genre__name__icontains=keyword) |
                      Q(description__icontains=keyword)
                )
        book_list = Book.objects.filter(query).distinct()
    search_form = SearchForm(request.GET or None)
    context = {
        'book_list': book_list,
        'search_form': search_form,
    }
    return render(request, 'books/search_books.html', context)


def feedback(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        send_feedback(
            form.cleaned_data['name'],
            form.cleaned_data['email'],
            form.cleaned_data['message'])
        return redirect('books:feedback_was_sent')
    context = {
        'form': form
    }
    return render(request, 'books/feedback.html', context)


def send_feedback(name, email, message):
    text = get_template('message.html')
    html = get_template('message.html')
    context = {
        'name': name,
        'email': email,
        'message': message
    }
    subject = 'Обратная связь'
    from_email = settings.EMAIL_HOST_USER
    text_content = text.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [settings.EMAIL_HOST_USER])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def feedback_was_sent(request):
    return render(request, 'books/feedback_was_sent.html')
