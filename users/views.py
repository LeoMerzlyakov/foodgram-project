from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from . import forms


User = get_user_model()


def register_user(request):
    form = forms.CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(
            request,
            message=f'Аккаунт {username} успешно создан'
        )
        return redirect('users:login')
    return render(request, 'registration.html', {'form': form})
