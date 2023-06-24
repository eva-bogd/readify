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

    # страница с прочитанными книгами
    path('book_read', views.book_read, name='book_read'),
    # добавить книгу в прочитанные
    path('books/<int:book_id>/add_book_read/', views.add_book_read,
         name='add_book_read'),
    # удалить книгу из прочитанных
    path('books/<int:book_id>/remove_book_read/', views.remove_book_read,
         name='remove_book_read'),

    # страница со списком запланированных книг
    path('book_to_read', views.book_to_read,
         name='book_to_read'),
    # добавить книгу в запланированные
    path('books/<int:book_id>/add_book_to_read/', views.add_book_to_read,
         name='add_book_to_read'),
    # удалить книгу из запланированных
    path('books/<int:book_id>/remove_book_to_read/', views.remove_book_to_read,
         name='remove_book_to_read'),

    # поиск по книгам
    path('search_books/', views.search_books, name='search_books'),
]
