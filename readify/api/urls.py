from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, AuthorViewSet, BookViewSet

router_api_v1 = DefaultRouter()

router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('authors', AuthorViewSet, basename='authors')
router_api_v1.register('books', BookViewSet, basename='books')
# router_api_v1.register('reviews', ReviewViewSet, basename='reviews')
# router_api_v1.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router_api_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
