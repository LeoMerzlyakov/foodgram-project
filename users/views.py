from django.contrib.messages.api import error
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model, views

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


# def loginview(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         # email = request.POST['email']
#         user = authenticate(
#             request=request,
#             username=username,
#             password=password,
#             # email=email,
#         )
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 messages.success(
#                     request,
#                     message=f'Пользователь {username} успешно вошёл!'
#                 )
#                 return redirect('/')
#             else:
#                 messages.warning(
#                     request,
#                     message=f'Пользователь {username} не активен!'
#                 )
#                 return redirect('/')
#         else:
#             messages.warning(
#                 request,
#                 message='Неверные данные'
#             )
#             return render(request, 'authForm.html', {})
#         # else:
#         #     return render(request, 'authForm.html', {'form': form})
#     else:
#         form = forms.LogInForm()
#         return render(request, 'authForm.html', {'form': form})
