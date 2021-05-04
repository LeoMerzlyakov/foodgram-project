from recipes.models import Ingredient, Favorite
from django.shortcuts import get_object_or_404

def get_ingredients(text_name):
    finded = Ingredient.objects.filter(ingredient__startswith=text_name)
    data = []
    for item in finded:
        data.append({'title': item.ingredient, 'dimension': item.unit})
    return data

def get_favor_note(pk, user):
    return get_object_or_404(Favorite, recipe=pk, user=user)
    