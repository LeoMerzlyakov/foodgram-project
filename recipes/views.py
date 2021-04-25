from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import context, loader
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from . import models, services, forms

User = get_user_model()

def recipes(request):
    recipes = models.Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'recipes': recipes, 'page': page, 'paginator': paginator}
    
    template = loader.get_template('indexAuth.html')
    return HttpResponse(template.render(context, request))


def user_recipes(request, user_id):
    recipes = models.Recipe.objects.filter(author=user_id)
    context = {'recipes': recipes}
    template = loader.get_template('authorRecipe.html')
    return HttpResponse(template.render(context, request))

@login_required
def favorites(request):
    """ Страница для вывода избранных записей текущего пользователя """
    recipes = models.Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'recipes': recipes, 'page': page, 'paginator': paginator}
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
            recipe = services.seve_recipe(request, form)
            return HttpResponseRedirect(reverse('recipes:recipe', 
                   kwargs={'recipe_id': recipe.id}))
        else:
            context = {'form': form}
            return render(request, 'formChangeRecipe.html', context)
    else:
        form = forms.RecipeForm(instance=recipe)
        for ingr in ingredients:
            i = ingr.ingredient.ingredient
            v = ingr.value
            u = ingr.ingredient.unit
        context = {'form': form, 'recipe': recipe, 'ingredients':ingredients}
        return render(request, 'formChangeRecipe.html', context)


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
            context = {'form': form}
            return render(request, 'formRecipe.html', context)
    else:
        form = forms.RecipeForm()
        context = {'form': form}
        return render(request, 'formRecipe.html', context)


@login_required
def follows(request):
    """Страница с отображением подписок"""
    recipe = models.Recipe.objects.all()
    context = {'recipes': recipe}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def purchases(request):
    """Страница с отображением покупок"""
    recipe = models.Recipe.objects.all()
    context = {'recipes': recipe}
    template = loader.get_template('favorite.html')
    return HttpResponse(template.render(context, request))


@login_required
def recipe(request, recipe_id):
    """Страница с отображением конкретного рецепта"""
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    ingrs = models.IngredientsValue.objects.filter(recipe=recipe.pk)
    context = {'recipe': recipe, 'ingredients': ingrs}
    template = loader.get_template('singlePage.html')
    return HttpResponse(template.render(context, request))
