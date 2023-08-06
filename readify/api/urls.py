from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet, AuthorViewSet, BookViewSet,
                    UserBookListViewSet)

router_api_v1 = DefaultRouter()

router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('authors', AuthorViewSet, basename='authors')
router_api_v1.register('books', BookViewSet, basename='books')
router_api_v1.register('users', UserBookListViewSet, basename='users')


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_api_v1.urls)),
    # path('users/<int:pk>/book_read/', CustomUserViewSet.as_view({'get': 'get_book_read'}), name='user-book-read')
]
