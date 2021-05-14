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
import json
import ast

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


def get_ingredients_and_values(user_id):
    ingredients = IngredientsValue.objects.filter(
        recipe__recipes_by_purchases__user_id=user_id
    ).all()

    shop_basket = {}
    for ingredient in ingredients:
        ingr_value = ingredient.value
        ingr_name = ingredient.ingredient.ingredient
        ingr_id = ingredient.ingredient.pk
        ingr_unit = ingredient.ingredient.unit
        if ingr_id not in shop_basket.keys():
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
        selected_tags = ['B', 'L', 'D']
    selected_tags = ''.join(selected_tags)
    return selected_tags
