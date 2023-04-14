from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # главная страница
    path('', views.home, name='home'),
    # страница с каталогом книг
    path('books/', views.books, name='books'),
    # страница с определенной книгой
    path('books/<int:book_id>/', views.books_detail, name='books_detail'),  # int: books_id
    # страница с книгами по жанру
    path('books/<slug:slug>/', views.books_genre, name='books_genre'),
    # страница с книгами автора
    path('author/<int:author_id>/', views.author, name='author'),
    # поиск по книгам
    path('search_books/', views.search_books, name='search_books'),
]
