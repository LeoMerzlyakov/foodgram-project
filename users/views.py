from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from . import forms


User = get_user_model()


def register_user(request):
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                message=f'Аккаунт {username} успено создан'
            )
            return redirect('users:login')
    else:
        form = forms.CreateUserForm()
    return render(request, 'registration.html', {'form': form})
