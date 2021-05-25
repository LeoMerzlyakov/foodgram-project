from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404

from recipes.models import (
    Ingredient,
    IngredientsValue,
    Recipe,
    Tag,
)


def get_ingredients(request):
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            int_value = post[f'valueIngredient_{num}'].partition(',')[0]
            ingredients[name] = int_value
    return ingredients


def ingr_validate(ingredients):
    for ingredient in ingredients:
        value = ingredients.get(ingredient)
        if not Ingredient.objects.filter(ingredient=ingredient).exists():
            return False, f'Ингредиента "{ingredient}" не существует'
        try:
            value = int(value)
        except ValueError:
            return False, f'Количество ингредиента "{ingredient}" \
                должно быть целым числом (введено {value})'
        if value < 1:
            return False, f'Количество ингредиента "{ingredient}" \
                должно быть не отрицательным (введено {value})'
    return True, 'OK'


def clean_ingredients(recipe_id):
    IngredientsValue.objects.filter(recipe=recipe_id).delete()


def clear_tags(recipe_id):
    if recipe_id:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.tags.clear()


def get_tags(request):
    tags = []
    post = request.POST
    if 'dinner' in post:
        tags.append(Tag.DINNER)
    if 'lunch' in post:
        tags.append(Tag.LUNCH)
    if 'breakfast' in post:
        tags.append(Tag.BREAKFAST)
    return tags


def seve_recipe(request, form, recipe_id=None):
    with transaction.atomic():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        tags = get_tags(request)
        clear_tags(recipe_id)
        for tag in tags:
            tag_obj = get_object_or_404(Tag, name=tag)
            new_recipe.tags.add(tag_obj)
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


def get_ingredients_and_values(user_id):
    ingredients = IngredientsValue.objects.filter(
        recipe__recipes_by_purchases__user_id=user_id
    )

    shop_basket = {}
    for ingredient in ingredients:
        ingr_value = ingredient.value
        ingr_name = ingredient.ingredient.ingredient
        ingr_id = ingredient.ingredient.pk
        ingr_unit = ingredient.ingredient.unit
        if ingr_id not in shop_basket:
            shop_basket[ingr_id] = (ingr_name, ingr_value, ingr_unit)
        else:
            current_name, current_value, current_unit = shop_basket[ingr_id]
            current_value = current_value + ingr_value
            shop_basket[ingr_id] = (current_name, current_value, current_unit)

    return shop_basket


def get_text(user_id):
    shop_basket = get_ingredients_and_values(user_id)
    header = 'Список покупок:'
    text = []
    for current_name, current_value, current_unit in shop_basket.values():
        row = current_name + ': ' + str(current_value) + ', ' + current_unit
        text.append(row)
    return header, text


def get_purchases_pdf(request):
    import io
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont('DejaVuSansCondensed', 'DejaVuSansCondensed.ttf')
    )

    header, text = get_text(request.user.id)
    p.setFont('DejaVuSansCondensed', 36)
    p.drawString(100, 700, header)

    y = 650
    p.setFont('DejaVuSansCondensed', 12)
    for row in text:
        p.drawString(100, y, row)
        y = y - 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def make_tag_context(request):
    if 'tags' in request.GET:
        selected_tags = request.GET['tags']
        selected_tags = list(selected_tags)
    else:
        selected_tags = [
            Tag.BREAKFAST,
            Tag.LUNCH,
            Tag.DINNER
        ]
    selected_tags = ''.join(selected_tags)
    return selected_tags


def get_paginator(request, obj_list):
    paginator = Paginator(obj_list, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return page, paginator


def get_form_name(instance_id):
    return 'edit_recipe' if instance_id else 'new_recipe'


def volidate_form_tags(data):
    tags = []
    if 'breakfast' in data:
        tags.append(Tag.BREAKFAST)
    if 'lunch' in data:
        tags.append(Tag.LUNCH)
    if 'dinner' in data:
        tags.append(Tag.DINNER)
    return (False if len(tags) < 1 else True) , tags
