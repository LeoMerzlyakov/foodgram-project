from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from . import views

app_name = 'users'
urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='authForm.html',),
         name='login'),
         
    path('logout/', 
         LogoutView.as_view(
             template_name='registration/logged_out.html',
             next_page='recipes:recipes'
         ),
         name='logout'),

    path('change_pass/', PasswordChangeView.as_view(
        template_name='changePassword.html',
        success_url = 'recipes:recipes',
    ), name='change_password'),

    path('reset_pass/', PasswordResetView.as_view(
        template_name='resetPassword.html',
        success_url = 'recipes:recipes',
    ), name='reset_password'),

    path('new/', views.NewUserView.as_view(), name='new_user'),
]