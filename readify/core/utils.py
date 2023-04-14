from django.core.paginator import Paginator


amount = 10


def get_paginator(request, book_list):
    paginator = Paginator(book_list, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
