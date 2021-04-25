from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, IngredientsValue, Tag
from django.db import transaction

def get_ingredients(request):
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients[name] = post[f'valueIngredient_{num}']
    return ingredients

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


def seve_recipe(request, form):
    with transaction.atomic():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        tags = get_tags(request)
        for tag in tags:
            tag_obj = Tag.objects.filter(tag=tag).first()
            new_recipe.tag.add(Tag.objects.get(id=tag_obj.id))
        new_recipe.save()
        

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
