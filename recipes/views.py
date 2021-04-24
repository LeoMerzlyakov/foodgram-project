from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import context, loader
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from . import models

User = get_user_model()

def recipes(request):
    recepies = models.Recipe.objects.all()
    context = {'recepies': recepies}
    
    if request.user.is_authenticated:
        template = loader.get_template('indexAuth.html')
    else:
        template = loader.get_template('indexNotAuth.html')
    return HttpResponse(template.render(context, request))


def user_recipes(request, user_id):
    recepies = models.Recipe.objects.filter(author=user_id)
    context = {'recepies': recepies}
    template = loader.get_template('authorRecipe.html')
    return HttpResponse(template.render(context, request))

@login_required
def favorites(request):
    recepies = models.Recipe.objects.all()
    context = {'recepies': recepies}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def edit_recipes(request, recipe_id):
    recepie = models.Recipe.objects.get(pk=recipe_id)
    context = {'recepies': recepie}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def create_recipe(request):
    """Страница с формой создания рецепта"""
    recepie = models.Recipe.objects.all()
    context = {'recepies': recepie}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def follows(request):
    """Страница с отображением подписок"""
    recepie = models.Recipe.objects.all()
    context = {'recepies': recepie}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def purchases(request):
    """Страница с отображением покупок"""
    recepie = models.Recipe.objects.all()
    context = {'recepies': recepie}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def recipe(request):
    """Страница с отображением конкретного рецепта"""
    recepie = models.Recipe.objects.all()
    context = {'recepies': recepie}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))
