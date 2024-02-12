from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AuthorViewSet, BookViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, UserBookListViewSet)

router_api_v1 = DefaultRouter()

router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('authors', AuthorViewSet, basename='authors')
router_api_v1.register('books', BookViewSet, basename='books')
router_api_v1.register('users', UserBookListViewSet, basename='users')
router_api_v1.register(
    r'^books/(?P<book_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
    )
router_api_v1.register(
    r'^books/(?P<book_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
    )


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_api_v1.urls))
]
