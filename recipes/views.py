from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.http.response import (
    Http404, HttpResponse, HttpResponseRedirect
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse

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
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render(context, request))


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
    # template = loader.get_template('author_recipe.html')
    # return HttpResponse(template.render(context, request))


@login_required
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
    # template = loader.get_template('favorite.html')
    # return HttpResponse(template.render(context, request))


@login_required
def edit_recipes(request, recipe_id):
    """Страница с формой редактирования рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    ingredients = models.IngredientsValue.objects.filter(recipe=recipe)

    form = forms.RecipeForm(
        request.POST or None ,
        instance=recipe,
        files=request.FILES or None
    )
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


@login_required
def create_recipe(request):
    """Страница с формой создания рецепта"""
    form = forms.RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        recipe = services.seve_recipe(request, form)
        return redirect('recipes:recipe', recipe_id=recipe.id)
    else:
        recipe = {}
        if form.data:
            recipe = {
                'title': form.data['title'],
                'image': form.data['image'],
                'description': form.data['description'],
                'cooking_time': form.data['cooking_time'],
            }
        page = services.get_form_name(form.instance.id)

        context = {
            'form': form,
            'recipe': recipe,
            'selected_page': page
        }
        return render(request, 'change_recipe.html', context)


@login_required
def follows(request):
    """Страница с отображением подписок"""

    authors = models.Follow.objects.filter(
        user=request.user.id
    ).all()

    paginator = Paginator(authors, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {
        'page': page,
        'paginator': paginator,
        'selected_page': 'follows',
    }
    return render(request, 'my_follows.html', context)
    # template = loader.get_template('my_follows.html')
    # return HttpResponse(template.render(context, request))


@login_required
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
    # template = loader.get_template('shop_list.html')
    # return HttpResponse(template.render(context, request))


@login_required
def purchases_delete(request, recipe_id):
    """Удалить рецепт из списка покупок"""
    user = request.user
    purchase = get_object_or_404(
        models.Purchase,
        user=user.id,
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
    # template = loader.get_template('shop_list.html')
    # return HttpResponse(template.render(context, request))


@login_required
def recipe(request, recipe_id):
    """Страница с отображением конкретного рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    ingrs = models.IngredientsValue.objects.filter(recipe=recipe.pk)
    context = {
        'recipe': recipe,
        'ingredients': ingrs,
    }
    return render(request, 'recipe_page.html', context)
    # template = loader.get_template('recipe_page.html')
    # return HttpResponse(template.render(context, request))


@login_required
def delete_recipe(request, recipe_id):
    """Страница с отображением конкретного рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('recipes:recipes')


def export_pdf(request):
    buffer = services.get_purchases_pdf(request)
    return FileResponse(buffer, as_attachment=True, filename='Purchases.pdf')


def page_not_found(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def forbidden(request, exception):
    response = render(request, '404.html')
    response.status_code = 403
    return response


def bed_request(request, exception):
    response = render(request, '404.html')
    response.status_code = 400
    return response


def interall_error(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response


def other_page(request, page):
    try:
        template = loader.get_template('flatpages/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return render(request, template.template.name)
