from django.contrib import admin

from .models import Genre, Author, Book, Review, Comment, BookRead, BookToRead


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'genre', 'year',)  # рейтинг добавить
    list_editable = ('author', 'genre', 'year',)
    # ordering = ('-rating')
    list_per_page = 10
    search_fields = ('name', 'author',)
    list_filter = ('name', 'author', 'genre', 'added_date',)
    empty_value_display = '-пусто-'


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(BookRead)
admin.site.register(BookToRead)
