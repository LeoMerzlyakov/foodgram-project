from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import context, loader
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

def index(request):
    recepies = models.Recipe.objects.all()
    context = {'recepies': recepies}
    
    if request.user.is_authenticated:
        template = loader.get_template('indexAuth.html')
    else:
        template = loader.get_template('indexNotAuth.html')
    return HttpResponse(template.render(context, request))
