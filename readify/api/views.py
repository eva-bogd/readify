from books.models import (Author, Book, BookRead, BookToRead, Comment, Genre,
                          Review)
from books.services import BookRecommendationService
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .filters import BookFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (AuthorSerializer, BookListSerializer,
                          BookReadSerializer, BookSerializer,
                          BookToReadSerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer)


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

    @action(methods=['get'],
            detail=False,
            url_path='recommendations',
            permission_classes=[IsAuthenticated])
    def get_recommendations(self, request):
        user = request.user
        queryset = BookRecommendationService.get_recommendations_for_user(
            user_id=user.id)
        serializer = BookListSerializer(queryset, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name',)
    filterset_class = BookFilter

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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # создание записи - авторизованные пользователи
    # изменение записи - автор записи или админ
    # остальные - только чтение
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        return Review.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book_id = self.kwargs.get('book_id')
        serializer.save(book_id=book_id, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # создание записи - авторизованные пользователи
    # изменение записи - автор записи или админ
    # остальные - только чтение
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(review_id=review_id, author=self.request.user)
