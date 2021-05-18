from recipes.models import Ingredient


def get_ingredients(text_name):
    finded = Ingredient.objects.filter(
        ingredient__startswith=text_name).values('ingredient', 'unit')
    data = []
    for item in finded:
        data.append({'title': item['ingredient'], 'dimension': item['unit']})
    return data
