from django import template
from django.shortcuts import get_object_or_404

from recipes.models import Favorite, Follow, Purchase, Recipe

from users.models import User


register = template.Library()


@register.simple_tag()
def is_in_purchase(user, recipe):
    return Recipe.objects.filter(
        recipes_by_purchases__user=user, recipes_by_purchases__recipe=recipe
    ).exists()


@register.simple_tag()
def is_favorite(user, recipe):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag()
def purchase_count(user):
    return Purchase.objects.filter(user=user).count()


@register.simple_tag()
def is_subscubed(user, author):
    if author != '':
        return Follow.objects.filter(user=user, author=author).exists()
    else:
        return False


@register.simple_tag()
def recipes_left(author):
    recipes_count = Recipe.objects.filter(author=author).count()
    return (recipes_count - 3 if recipes_count > 3 else 0)


@register.simple_tag()
def get_recipe_by_author_id(author_id):
    return Recipe.objects.filter(author=author_id).all()


@register.simple_tag()
def get_main_header_name(page_name, author_id=''):
    if page_name == 'author':
        if author_id != '':
            return get_object_or_404(User, pk=author_id)
        else:
            return ''
    elif page_name == 'recipes':
        return 'Рецепты'
    elif page_name == 'favorites':
        return 'Избранное'
    elif page_name == 'follows':
        return 'Мои подписки'
    elif page_name == 'purchases':
        return 'Список покупок'
    elif page_name == 'new_recipe':
        return 'Создание рецепта'
    elif page_name == 'edit_recipe':
        return 'Редактирование рецепта'    
    return 'Unnamed page!'


@register.simple_tag()
def get_url_page(page_name):
    if page_name == 'author':
        return 'recipes:recipes_by_author'
    elif page_name == 'recipes':
        return 'recipes:recipes'
    elif page_name == 'favorites':
        return 'recipes:favorites'
    return 'Unnamed page!'
