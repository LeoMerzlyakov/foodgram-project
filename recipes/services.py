from django.shortcuts import get_object_or_404
from recipes.models import (
    Ingredient,
    IngredientsValue,
    Recipe,
    Tag,
    Favorite,
    Purchase,
)
from django.db import transaction

def get_ingredients(request):
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            int_value = post[f'valueIngredient_{num}'].partition(',')[0]
            ingredients[name] = int_value
    return ingredients

def clean_ingredients(recipe_id):
    IngredientsValue.objects.filter(recipe=recipe_id).delete()


def clear_tags(recipe_id):
    if recipe_id:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.tags.clear()


def is_favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


def is_in_purchase(recipe, user):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


def get_tags(request):
    tags = []
    post = request.POST
    if 'dinner' in post.keys():
        tags.append('D')
    if 'lunch' in post.keys():
        tags.append('L')    
    if 'breakfast' in post.keys():
        tags.append('B')
    return tags


def seve_recipe(request, form, recipe_id=None):
    with transaction.atomic():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        tags = get_tags(request)
        clear_tags(recipe_id)
        for tag in tags:
            tag_obj = Tag.objects.filter(name=tag).first()
            new_recipe.tags.add(Tag.objects.get(id=tag_obj.id))
        new_recipe.save()
        
        if recipe_id:
            clean_ingredients(recipe_id)
        ingredient_list = []
        ingredients = get_ingredients(request)
        for name, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, ingredient=name)
            ingredient_list.append(
                IngredientsValue(
                    recipe=new_recipe,
                    ingredient=ingredient,
                    value=quantity
                )
            )
        IngredientsValue.objects.bulk_create(ingredient_list)
        form.save_m2m()
        return new_recipe
