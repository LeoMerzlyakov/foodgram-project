from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username',)


class LogInForm(AuthenticationForm):
    email = forms.EmailField()
    password = forms.PasswordInput()

    class Meta():
        model = User
        fields = ('email', 'password', 'username', )
