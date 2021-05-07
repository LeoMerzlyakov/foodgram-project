from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users."""
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='username', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class UserChangeForm(forms.ModelForm):
    """A form for updating users."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    """A form to add and change user instances.""" 
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_admin', 'email')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', )}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'is_admin'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
