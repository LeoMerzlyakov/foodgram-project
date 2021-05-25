from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetView)
from django.urls import path, reverse_lazy

from . import views


app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='login.html',
    ), name='login'),

    path('logout/', LogoutView.as_view(
        template_name='registration/logged_out.html',
        next_page='recipes:recipes'
    ), name='logout'),

    path('change_pass/', PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url=reverse_lazy('recipes:recipes'),
    ), name='change_password'),

    path('change_pass/done/', PasswordChangeDoneView.as_view(
        template_name='customPage.html',
    ), name='password_change_done'),

    path('reset_pass/', PasswordResetView.as_view(
        success_url=reverse_lazy('users:password_reset_done'),
        template_name='reset_password.html',
        subject_template_name = 'password_reset_subject.txt',
        email_template_name = 'password_reset_email.html',
    ), name='reset_password'),

    path('reset_pass_sent/', PasswordResetDoneView.as_view(
        template_name='reset_password_done.html'
    ), name='password_reset_done'),

    path('reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('users:password_reset_complete'),
        template_name = 'password_reset_confirm_custom.html',
    ), name='password_reset_confirm'),

    path('reset_pass_complete/', PasswordResetCompleteView.as_view(
        template_name = 'password_reset_complete.html'
    ),
        name='password_reset_complete'
    ),

    path('register/', views.register_user, name='register'),
]
