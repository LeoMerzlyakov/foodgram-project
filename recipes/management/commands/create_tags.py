from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Create TAGS (Breakfast, Lunch, Dinner).'

    def handle(self, *args, **options):
        Tag.objects.create(name=Tag.BREAKFAST)
        Tag.objects.create(name=Tag.LUNCH)
        Tag.objects.create(name=Tag.DINNER)
