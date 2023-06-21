from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import get_user_model

from django.contrib.auth import update_session_auth_hash

from books.models import Book, BookRead, BookToRead
from core.utils import get_paginator
from .forms import CreationForm, ProfileUpdateForm, PasswordChangingForm

# from django.conf import settings
# from django.core.mail import send_mail

from django.http import HttpResponse


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        username = self.request.POST['username']
        return reverse_lazy('users:profile', kwargs={'username': username})

@login_required
def profile(request, username):
    if request.method == 'POST':
        user = request.user
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user)
        if profile_form.is_valid():
            profile_form.save()
            # messages.success(request, "Профиль был успешно обновлён!")
            return redirect('users:profile', username=user.username)
    else:
        user = get_object_or_404(User, username=username)
        profile_form = ProfileUpdateForm(instance=user)
    context = {
        'user': user,
        'profile_update_form': profile_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def bookread(request):
    book_list = Book.objects.filter(books_read__user=request.user)
    context = {
        'page_obj': get_paginator(request, book_list)
    }
    return render(request, 'users/bookread.html', context)


@login_required
def booktoread(request):
    book_list = Book.objects.filter(books_to_read__user=request.user)
    context = {
         'page_obj': get_paginator(request, book_list)
    }
    return render(request, 'users/booktoread.html', context)

# send_mail(
#            'Восстановление пароля',
#            'Пожалуйста, перейдите по ссылке, чтобы сбросить ваш пароль',
#            settings.DEFAULT_FROM_EMAIL,
#            ['to@example.com'],
#            fail_silently=False,
#         )
