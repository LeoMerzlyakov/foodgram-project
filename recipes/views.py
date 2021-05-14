from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import context, loader
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.defaultfilters import join
from django.urls import reverse
from . import models, services, forms

User = get_user_model()

def recipes(request):
    selected_tags = services.make_tag_context(request)
    recipes = models.Recipe.objects.filter(
        tags__name__in=selected_tags
    ).distinct()

    paginator = Paginator(recipes, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    
    context = {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': selected_tags,
        'selected_page': 'recipes'
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def user_recipes(request, user_id):
    selected_tags = services.make_tag_context(request)
    recipes = models.Recipe.objects.filter(
        author=user_id,
        tags__name__in=selected_tags
    ).distinct()
        
    paginator = Paginator(recipes, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
        
    context = {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': selected_tags,
        'selected_page': 'author'
    }
    template = loader.get_template('author_recipe.html')
    return HttpResponse(template.render(context, request))

@login_required
def favorites(request):
    """ Страница для вывода избранных записей текущего пользователя """
    selected_tags = services.make_tag_context(request)
    recipes = models.Recipe.objects.filter(
        favorites_recipes__user=request.user.id,
        tags__name__in=list(selected_tags)
    ).distinct()

    paginator = Paginator(recipes, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': selected_tags,
        'selected_page': 'favorites',
    }
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def edit_recipes(request, recipe_id):
    """Страница с формой редактирования рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    ingredients = models.IngredientsValue.objects.filter(recipe=recipe)
    if request.method == 'POST':
        form = forms.RecipeForm(
            request.POST,
            instance=recipe,
            files=request.FILES or None
        )
        if form.is_valid():
            recipe = services.seve_recipe(request, form, recipe_id)
            return HttpResponseRedirect(reverse('recipes:recipe', 
                   kwargs={'recipe_id': recipe.id}))
        else:
            context = {'form': form}
            return render(request, 'change_recipe.html', context)
    else:
        form = forms.RecipeForm(instance=recipe)
        tags = recipe.tags.values_list('name', flat=True)
        context = {
            'form': form,
            'recipe': recipe,
            'ingredients': ingredients,
            'tags': tags,
        }
        return render(request, 'change_recipe.html', context)


@login_required
def create_recipe(request):
    """Страница с формой создания рецепта"""
    if request.method == 'POST':
        form = forms.RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            recipe = services.seve_recipe(request, form)
            return HttpResponseRedirect(reverse('recipes:recipe', 
                   kwargs={'recipe_id': recipe.id}))
        else:
            context = {
                'form': form,
                'selected_page': 'new_recipe'
            }
            return render(request, 'create_recipe.html', context)
    else:
        form = forms.RecipeForm()
        context = {
                'form': form,
                'selected_page': 'new_recipe'
            }
        return render(request, 'create_recipe.html', context)


@login_required
def follows(request):
    """Страница с отображением подписок"""
    recipes = models.Recipe.objects.filter(
        author__author_is_followed__user=request.user.id
    ).all().order_by('author')

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
        'selected_page': 'follows',
        'page': page,
        'paginator': paginator,
        'selected_page': 'follows',
    }
    template = loader.get_template('my_follows.html')
    return HttpResponse(template.render(context, request))


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
    template = loader.get_template('shop_list.html')
    return HttpResponse(template.render(context, request))

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
    template = loader.get_template('shopList.html')
    return HttpResponse(template.render(context, request))


@login_required
def recipe(request, recipe_id):
    """Страница с отображением конкретного рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    ingrs = models.IngredientsValue.objects.filter(recipe=recipe.pk)
    is_favorite = services.is_favorite(recipe_id, request.user.id)
    context = {
        'recipe': recipe,
        'ingredients': ingrs,
        'is_favorite': is_favorite,
    }
    template = loader.get_template('recipe_page.html')
    return HttpResponse(template.render(context, request))


@login_required
def delete_recipe(request, recipe_id):
    """Страница с отображением конкретного рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('recipes:recipes')


def export_pdf(request):
    buffer = services.get_purchases_pdf(request)
    return FileResponse(buffer, as_attachment=True, filename='Purchases.pdf')


def custom404(request, exception):
    return render(request, 'error_pages/404.html')


def custom500(request, exception):
    return render(request, 'error_pages/500.html')
