from django.db.models import F
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient
from users.models import User


def get_ingredients(text_name):
    return list(
        Ingredient.objects.filter(
            ingredient__startswith=text_name
            ).values(title=F('ingredient'), dimension=F('unit'))
    )


def get_author_instance(param):
    try:
        param = int(param)
        return get_object_or_404(User, pk=param)
    except ValueError:
        return get_object_or_404(User, username=param)
