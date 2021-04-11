from django.forms import ModelForm, fields, widgets
from django import forms
from .models import User


class UserForm(ModelForm):
    email = forms.EmailField(
        label='your email',
        help_text="a message will be sent to this email",
        initial='your@email.com'
    )
    login = forms.CharField(
        label='your name',
    )
    password = forms.CharField(
        widget=forms.widgets.PasswordInput,
        label='your password',
        help_text="don't forget it!",
    )

    class Meta:
        model = User
        fields = ('email','login','password',)
