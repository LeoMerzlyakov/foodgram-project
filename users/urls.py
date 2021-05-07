from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import include, path, reverse_lazy, reverse
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView)
from django.urls.base import reverse
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='authForm.html',
    ), name='login'),

    path('logout/', LogoutView.as_view(
        template_name='registration/logged_out.html',
        next_page='recipes:recipes'
    ), name='logout'),

    path('change_pass/', PasswordChangeView.as_view(
        template_name='changePassword.html',
        success_url = reverse_lazy('recipes:recipes'),
        # success_url = reverse_lazy('users:password_change_done')
    ), name='change_password'),

    path('change_pass/done/', PasswordChangeDoneView.as_view(
        template_name='customPage.html',
    ), name='password_change_done'),

    path('reset_pass/', PasswordResetView.as_view(
        template_name='resetPassword.html',
        success_url = 'recipes:recipes',
    ), name='reset_password'),

    path('register/', views.register_user, name='register'),
]
