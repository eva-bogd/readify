from django.contrib import admin

from .models import Genre, Author, Book, Review, Comment, BookRead, BookToRead


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'year', 'rating_display')
    list_editable = ('author', 'year',)
    filter_horizontal = ('genre',)
    # ordering = ('-rating')
    list_per_page = 10
    search_fields = ('name', 'author',)
    list_filter = ('name', 'author', 'genre', 'added_date',)
    empty_value_display = '-пусто-'

    def rating_display(self, obj):
        return obj.rating
    rating_display.short_description = 'Рейтинг'


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(BookRead)
admin.site.register(BookToRead)
