from books.models import Book, Genre
from django_filters import rest_framework as filters


class BookFilter(filters.FilterSet):
    genre = filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        field_name='genre__name',
        to_field_name='name'
        )
    author = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains'
        )
    is_read = filters.BooleanFilter(
        method='filter_is_read_by_user'
        )
    is_planned = filters.BooleanFilter(
        method='filter_is_planned_by_user'
        )

    class Meta:
        model = Book
        fields = ['genre', 'author', 'is_read', 'is_planned']

    def filter_is_read_by_user(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        if value:
            return queryset.filter(books_read__user=user)
        return queryset.exclude(books_read__user=user)

    def filter_is_planned_by_user(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        if value:
            return queryset.filter(books_to_read__user=user)
        return queryset.exclude(books_to_read__user=user)
