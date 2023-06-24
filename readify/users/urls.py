from django.urls import path
from . import views

from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)


app_name = 'users'

urlpatterns = [
    # страница профиля пользователя
    path('profile/<str:username>', views.profile, name='profile'),
    # страница регистрации
    path('signup/', views.SignUp.as_view(), name='signup'),
    # страница входа
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    # cтраница выхода
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    # страница смены пароля
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change'
    ),
    # подтверждение смены пароля
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    # страница восстановления пароля
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html'),
        name='password_reset'
    ),
    # уведомление об отправке письма для восстановления пароля
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    # страница подтверждения сброса пароля (переходим по ссылке из письма)
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    # уведомление о том, что пароль изменен
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    )
]
