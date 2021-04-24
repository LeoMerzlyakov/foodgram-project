from django.forms import ModelForm, fields, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email','login','password',)


class LogInForm(ModelForm):
    login = forms.CharField(
        label='your name',
        initial='required'
    )
    password = forms.CharField(
        widget=forms.widgets.PasswordInput,
        label='your password',
        help_text="don't forget it!",
        initial='required'
    )

    class Meta:
        model = User
        fields = ('login','password',)
