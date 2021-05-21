from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms.forms import Form
from django.http import FileResponse
from django.http.response import (Http404)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist

from . import forms, models, services

User = get_user_model()


def recipes(request):
    selected_tags = services.make_tag_context(request)
    recipes = models.Recipe.objects.filter(
        tags__name__in=selected_tags
    ).distinct()
    
    page, paginator = services.get_paginator(request, recipes)

    context = {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': selected_tags,
        'selected_page': 'recipes'
    }

    return render(request, 'index.html', context)


def user_recipes(request, user_id):
    selected_tags = services.make_tag_context(request)
    recipes = models.Recipe.objects.filter(
        author=user_id,
        tags__name__in=selected_tags
    ).distinct()

    page, paginator = services.get_paginator(request, recipes)

    context = {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': selected_tags,
        'selected_page': 'author'
    }
    return render(request, 'author_recipe.html', context)


@login_required(redirect_field_name='next', login_url='/auth/login/')
def favorites(request):
    """ Страница для вывода избранных записей текущего пользователя """
    selected_tags = services.make_tag_context(request)
    recipes = models.Recipe.objects.filter(
        favorites_recipes__user=request.user.id,
        tags__name__in=list(selected_tags)
    ).distinct()

    page, paginator = services.get_paginator(request, recipes)

    context = {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': selected_tags,
        'selected_page': 'favorites',
    }
    return render(request, 'favorite.html', context)


@login_required(redirect_field_name='next', login_url='/auth/login/')
def edit_recipes(request, recipe_id):
    """Страница с формой редактирования рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    ingredients = models.IngredientsValue.objects.filter(recipe=recipe)
    form = forms.RecipeForm(
        request.POST or None ,
        instance=recipe,
        files=request.FILES or None
    )
    if not services.volidate_form_tags(request.POST):
        form.errors['tags'] = 'Выбирите один из вариантов!'
    if form.is_valid():
        recipe = services.seve_recipe(request, form, recipe_id)
        return redirect('recipes:recipe', recipe_id=recipe.id)
    else:
        page = services.get_form_name(form.instance.id)
        tags = recipe.tags.values_list('name', flat=True)
        context = {
            'form': form,
            'recipe': recipe,
            'ingredients': ingredients,
            'tags': tags,
            'selected_page': page
        }
        return render(request, 'change_recipe.html', context)


@login_required(redirect_field_name='next', login_url='/auth/login/')
def create_recipe(request):
    """Страница с формой создания рецепта"""
    form = forms.RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if not services.volidate_form_tags(request.POST) and request.method == 'POST':
        form.errors['tags'] = 'Выбирите один из вариантов!'
    if form.is_valid():
        recipe = services.seve_recipe(request, form)
        return redirect('recipes:recipe', recipe_id=recipe.id)
    else:
        recipe = {}
        if form.data:
            recipe = {
                'title': form.data.get('title'),
                'image': form.data.get('image'),
                'description': form.data.get('description'),
                'cooking_time': form.data.get('cooking_time'),
            }
        page = services.get_form_name(form.instance.id)

        context = {
            'form': form,
            'recipe': recipe,
            'selected_page': page
        }
        return render(request, 'change_recipe.html', context)


@login_required(redirect_field_name='next', login_url='/auth/login/')
def follows(request):
    """Страница с отображением подписок"""

    authors = models.Follow.objects.filter(user=request.user.id)
    page, paginator = services.get_paginator(request, authors)
    context = {
        'page': page,
        'paginator': paginator,
        'selected_page': 'follows',
    }
    return render(request, 'my_follows.html', context)


@login_required(redirect_field_name='next', login_url='/auth/login/')
def purchases(request):
    """Страница с отображением покупок"""
    recipes = models.Recipe.objects.filter(
        recipes_by_purchases__user=request.user.id
    )
    context = {
        'recipes': recipes,
        'selected_page': 'purchases'
    }
    return render(request, 'shop_list.html', context)


@login_required(redirect_field_name='next', login_url='/auth/login/')
def purchases_delete(request, recipe_id):
    """Удалить рецепт из списка покупок"""
    purchase = get_object_or_404(
        models.Purchase,
        user=request.user.id,
        recipe_id=recipe_id
    )
    purchase.delete()
    recipes = models.Recipe.objects.filter(
        recipes_by_purchases__user=request.user.id
    )
    context = {
        'recipes': recipes,
        'selected_page': 'purchases'
    }
    return render(request, 'shop_list.html', context)


def recipe(request, recipe_id):
    """Страница с отображением конкретного рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    ingrs = models.IngredientsValue.objects.filter(recipe=recipe.pk)
    context = {
        'recipe': recipe,
        'ingredients': ingrs,
    }
    return render(request, 'recipe_page.html', context)


@login_required(redirect_field_name='next', login_url='/auth/login/')
def delete_recipe(request, recipe_id):
    """Страница с отображением конкретного рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('recipes:recipes')


def export_pdf(request):
    buffer = services.get_purchases_pdf(request)
    return FileResponse(buffer, as_attachment=True, filename='Purchases.pdf')


def other_page(request, page):
    try:
        template = loader.get_template('flatpages/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return render(request, template.template.name)
