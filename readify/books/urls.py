from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),

    path('books/', views.books, name='books'),
    path('books/<int:book_id>/', views.books_detail, name='books_detail'),
    path('books/<slug:slug>/', views.books_genre, name='books_genre'),
    path('books/author/<int:author_id>/', views.book_author, name='author'),

    path('books/<int:book_id>/add_review>', views.add_review,
         name='add_review'),
    path('books/<int:book_id>/reviews/<int:review_id>/edit', views.edit_review,
         name='edit_review'),
    path('books/<int:book_id>/reviews/<int:review_id>/add_comment',
         views.add_comment, name='add_comment'),
    path('books/<int:book_id>/reviews/<int:review_id>/comments/<int:comment_id>/edit_comment',
         views.edit_comment, name='edit_comment'),


    path('users/<int:user_id>/book_read/', views.book_read, name='book_read'),
    path('books/<int:book_id>/add_book_read/', views.add_book_read,
         name='add_book_read'),
    path('books/<int:book_id>/remove_book_read/', views.remove_book_read,
         name='remove_book_read'),

    path('users/<int:user_id>/book_to_read/', views.book_to_read,
         name='book_to_read'),
    path('books/<int:book_id>/add_book_to_read/', views.add_book_to_read,
         name='add_book_to_read'),
    path('books/<int:book_id>/remove_book_to_read/', views.remove_book_to_read,
         name='remove_book_to_read'),

    path('books/recommendations', views.recommendations,
         name='recommendations'),

    path('search_books/', views.search_books, name='search_books'),

    path('feedback/', views.feedback, name='feedback'),
    path('feedback_was_sent/', views.feedback_was_sent,
         name='feedback_was_sent'),
]
