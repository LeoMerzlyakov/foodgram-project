from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv


class Command(BaseCommand):
    
    help = 'Load list of Ingredients.'\
           'Write "python manage.py load_ingredients" command to load data'

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv', encoding="utf-8") as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, unit = row
                Ingredient.objects.get_or_create(ingredient=name, unit=unit)
