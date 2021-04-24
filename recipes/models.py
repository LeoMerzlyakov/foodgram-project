from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET('deleted'),
        related_name='recipts_by_author',
        verbose_name='recipe author',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='recipe name',
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='recipe photo',
    )
    description = models.TextField(
        verbose_name='recipe description',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipts_by_ingredients',
        verbose_name='ingredients for recipe',
        through='IngredientsValue'
    )
    tag = models.ManyToManyField(
        'TAG',
        related_name='recipts_by_tag',
        verbose_name='tag for recipe',
    )
    slug = models.SlugField()
    cooking_time = models.IntegerField(verbose_name='cooking time')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    
    class Meta:
        verbose_name = 'recipe by author'
        verbose_name_plural = 'recipes by author'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class IngredientsValue(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Tag(models.Model):
    TAG = (
        ('B', 'breakfast'),
        ('L', 'lunch'),
        ('D', 'dinner'),
    )
    tag = models.CharField(
        max_length=1,
        choices=TAG,
    )


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=255)
    unit = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.ingredient}, {self.unit}'
