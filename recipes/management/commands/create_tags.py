from os import name
from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    
    help = 'Create TAGS (Breakfast, Lunch, Dinner).'

    def handle(self, *args, **options):
        Tag.objects.create(name='B')
        Tag.objects.create(name='L')
        Tag.objects.create(name='D')