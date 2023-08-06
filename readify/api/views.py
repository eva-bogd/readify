from django.shortcuts import render, get_object_or_404
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


class UserBookListViewSet(viewsets.ViewSet):
    lookup_field = 'user_id'

    @action(methods=['get'], detail=True, url_path='book_read')
    def get_book_read(self, request, user_id):
        user = request.user
        owner = get_object_or_404(User, id=user_id)
        if user.id != owner.id and owner.show_book_read is False:
            return Response("Список прочитанных книг недоступен",
                            status=status.HTTP_403_FORBIDDEN)
        queryset = BookRead.objects.filter(user_id=owner.id)
        serializer = BookReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='book_to_read')
    def get_book_to_read(self, request, user_id):
        user = request.user
        owner = get_object_or_404(User, id=user_id)
        if user.id != owner.id and owner.show_book_to_read is False:
            return Response("Список запланированных книг недоступен",
                            status=status.HTTP_403_FORBIDDEN)
        queryset = BookToRead.objects.filter(user_id=owner.id)
        serializer = BookToReadSerializer(queryset, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    # все действия кроме чтения только админ
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


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
        book_read = BookRead.objects.filter(book=book, user=user)
        if request.method == 'POST':
            if book_read.exists():
                return Response("Книга уже есть в списке прочитанных",
                                status=status.HTTP_400_BAD_REQUEST)
            new_book_read = BookRead.objects.create(book=book, user=user)
            BookReadSerializer(new_book_read)
            return Response("Книга добавлена в список прочитанных",
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not book_read.exists():
                return Response("Книга отсутствует в списке прочитанных",
                                status=status.HTTP_404_NOT_FOUND)
            book_read.delete()
            return Response("Книга удалена из списка прочитанных",
                            status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='book_to_read',
            permission_classes=[IsAuthenticated])
    def add_or_delete_in_book_to_read(self, request, pk=None):
        book = self.get_object()
        user = request.user
        book_to_read = BookToRead.objects.filter(book=book, user=user)
        if request.method == 'POST':
            if book_to_read.exists():
                return Response("Книга уже есть в списке запланированных",
                                status=status.HTTP_400_BAD_REQUEST)
            new_book_to_read = BookToRead.objects.create(book=book, user=user)
            BookToReadSerializer(new_book_to_read)
            return Response("Книга добавлена в список запланированных",
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not book_to_read.exists():
                return Response("Книга отсутствует в списке запланированных",
                                status=status.HTTP_404_NOT_FOUND)
            book_to_read.delete()
            return Response("Книга удалена из списка запланированных",
                            status=status.HTTP_204_NO_CONTENT)
