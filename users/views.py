from django.forms import fields
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from . import forms

User = get_user_model()

def create_user(request):
    if request.method == 'POST':
        user_form = forms.CreateUserForm()
        if user_form.is_valid():
            user_form.save()
            return render (request, 'reg.html')
        else:
            context = {'form': user_form}
            return render (request, 'reg.html', context=context)
    else:
        user_form = forms.CreateUserForm()
        context = {'form': user_form}
        return render (request, 'reg.html', context=context)


class NewUserView(CreateView):
    user_form = forms.CreateUserForm
    success_url = '/'
    template_name = 'reg.html'
    fields = ('email','login','password')

    def get_queryset(self):
        return User.objects.order_by('id')
        

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
        return render (request, 'authForm.html', {'from': user_form})
    else:
        user_form = forms.LogInForm()
        context = {'form': user_form}
        return render (request, 'authForm.html', context=context)
