from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import get_user_model

from .forms import CreationForm, ProfileUpdateForm

# from django.conf import settings
# from django.core.mail import send_mail


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
            instance=user)  # поля будут автоматически заполнены значениями
                            # из переданного объекта user
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


# send_mail(
#            'Восстановление пароля',
#            'Пожалуйста, перейдите по ссылке, чтобы сбросить ваш пароль',
#            settings.DEFAULT_FROM_EMAIL,
#            ['to@example.com'],
#            fail_silently=False,
#         )
