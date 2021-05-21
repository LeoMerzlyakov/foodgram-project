from django.db import models
from django.db.models.deletion import CASCADE

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes_by_author',
        verbose_name='recipe author',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='recipe name',
    )
    image = models.ImageField(
        blank=False,
        null=False,
        verbose_name='recipe photo',
    )
    description = models.TextField(
        verbose_name='recipe description',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes_by_ingredients',
        verbose_name='ingredients for recipe',
        through='IngredientsValue'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes_by_tag',
        verbose_name='tag for recipe',
    )
    slug = models.SlugField()
    cooking_time = models.PositiveIntegerField(
        verbose_name='cooking time'
    )
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
    BREAKFAST = 'B'
    LUNCH = 'L'
    DINNER = 'D'

    TAG_CHOISE = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    name = models.CharField(
        max_length=1,
        choices=TAG_CHOISE,
        verbose_name='Tag name (Breakfast/Lunch/Dinner)'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag name'
        verbose_name_plural = 'Tag names'
        ordering = ['-id']


class Ingredient(models.Model):
    ingredient = models.CharField(
        max_length=255,
        verbose_name='ingredient name'
    )
    unit = models.CharField(max_length=64, verbose_name='ingredient units')

    def __str__(self):
        return f'{self.ingredient}, {self.unit}'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['-id']


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name="favorites_recipes",
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique Favorite instance'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_which_follow",
                             blank=False,
                             null=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="author_is_followed",
                               blank=True,
                               null=True)

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='unique Follow instance'
            )
        ]


class Purchase(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="purchase_by_user",
                             blank=False,
                             null=True)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="recipes_by_purchases",
                               blank=True,
                               null=True)

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique Purchase instance'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'
