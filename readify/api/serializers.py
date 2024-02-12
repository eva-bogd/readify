from books.models import (Author, Book, BookRead, BookToRead, Comment, Genre,
                          Review)
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'birth_date', 'gender', 'avatar')


class CustomUserCreateSerializer(UserCreateSerializer):
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name', 'birth_date', 'gender', 'avatar')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(many=True, read_only=True)
    cover = Base64ImageField(required=False)
    in_book_read = serializers.SerializerMethodField()
    in_book_to_read = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'genre', 'rating',
                  'in_book_read', 'in_book_to_read',
                  'year', 'description', 'cover', 'added_date')

    def get_in_book_read(self, obj):
        user = self.context['request'].user
        return BookRead.objects.filter(
            user_id=user.id, book_id=obj.id).exists()

    def get_in_book_to_read(self, obj):
        user = self.context['request'].user
        return BookToRead.objects.filter(
            user_id=user.id, book_id=obj.id).exists()


class BookListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(many=True, read_only=True)
    cover = Base64ImageField(required=False)

    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'genre', 'rating', 'cover')


class BookReadSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BookRead
        fields = ('id', 'book', 'user', 'added_date')


class BookToReadSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BookToRead
        fields = ('id', 'book', 'user', 'added_date')


class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    def validate(self, attrs):
        if self.context['request'].method == "POST":
            author = self.context['request'].user
            book = get_object_or_404(
                Book,
                id=self.context['view'].kwargs.get('book_id')
            )
            if Review.objects.filter(
                book_id=book.id,
                author_id=author.id
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже оставили отзыв на эту книгу.")
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'book', 'author', 'text', 'score',
                  'added_date', 'edited_date')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    author = serializers.StringRelatedField(read_only=True)

    def validate(self, attrs):
        get_object_or_404(
            Review,
            book_id=self.context['view'].kwargs.get('book_id'),
            id=self.context['view'].kwargs.get('review_id')
        )
        return attrs

    class Meta:
        model = Comment
        fields = ('id', 'review', 'author', 'text',
                  'added_date', 'edited_date')
