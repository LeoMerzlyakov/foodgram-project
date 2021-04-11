from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users."""
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    login = forms.CharField(label='Login', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('email', 'login', 'password')


class UserChangeForm(forms.ModelForm):
    """A form for updating users."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'login', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    """A form to add and change user instances.""" 
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'login', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', )}),
        ('Personal info', {'fields': ('login',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'login', 'password', 'is_admin'),
        }),
    )

    search_fields = ('email', 'login')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
