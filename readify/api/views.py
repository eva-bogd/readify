from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from users.models import User
from books.models import (Genre, Author, Book, Review, Comment,
                          BookRead, BookToRead)
from .serializers import (CustomUserSerializer, GenreSerializer,
                          AuthorSerializer, BookSerializer, BookListSerializer,
                          BookReadSerializer, BookToReadSerializer)
from .permissions import IsAdminOrReadOnly


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    # все действия кроме чтения только админ
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    # все действия кроме чтения только админ
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    # все действия кроме чтения только админ
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='book_read',
            permission_classes=[IsAuthenticated])
    def add_or_delete_in_book_read(self, request, pk=None):
        book = self.get_object()
        user = request.user
        if request.method == 'POST':
            if BookRead.objects.filter(book=book, user=user).exists():
                return Response("Книга уже есть в списке прочитанных",
                                status=status.HTTP_400_BAD_REQUEST)
            book_read = BookRead.objects.create(book=book, user=user)
            BookReadSerializer(book_read)
            return Response("Книга добавлена в список прочитанных",
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not BookRead.objects.filter(book=book, user=user).exists():
                return Response("Книга отсутствует в списке прочитанных",
                                status=status.HTTP_404_NOT_FOUND)
            BookRead.objects.filter(book=book, user=user).delete()
            return Response("Книга удалена из списка прочитанных",
                            status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='book_to_read',
            permission_classes=[IsAuthenticated])
    def add_or_delete_in_book_to_read(self, request, pk=None):
        book = self.get_object()
        user = request.user
        if request.method == 'POST':
            if BookToRead.objects.filter(book=book, user=user).exists():
                return Response("Книга уже есть в списке запланированных",
                                status=status.HTTP_400_BAD_REQUEST)
            book_to_read = BookToRead.objects.create(book=book, user=user)
            BookToReadSerializer(book_to_read)
            return Response("Книга добавлена в список запланированных",
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not BookToRead.objects.filter(book=book, user=user).exists():
                return Response("Книга отсутствует в списке запланированных",
                                status=status.HTTP_404_NOT_FOUND)
            BookToRead.objects.filter(book=book, user=user).delete()
            return Response("Книга удалена из списка запланированных",
                            status=status.HTTP_204_NO_CONTENT)
