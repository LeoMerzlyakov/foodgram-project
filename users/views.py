from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from . import forms


def create_user(request):
    if request.method == 'POST':
        user_form = forms.CreateUserForm()
        if user_form.is_valid():
            user_form.save()
            return render (request, 'reg.html')
        else:
            context = {'form': user_form}
    else:
        user_form = forms.CreateUserForm()
        context = {'form': user_form}
        return render (request, 'reg.html', context=context)


def login(request):
    if request.method == 'POST':
        user_form = forms.LogInForm()
        if user_form.is_valid():
            username = user_form.cleaned_data['login']
            password = user_form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password,
            )
            if user:
                login(user)
                return HttpResponseRedirect('/')
            else:
                pass
        return render (request, 'authForm.html', {'from': user_form})
    else:
        user_form = forms.LogInForm()
        context = {'form': user_form}
        return render (request, 'authForm.html', context=context)
