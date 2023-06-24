from django import template

register = template.Library()


@register.filter
def is_book_read_by_user(book, user):
    return book.books_read.filter(user=user).exists()


@register.filter
def is_book_to_read_by_user(book, user):
    return book.books_to_read.filter(user=user).exists()
