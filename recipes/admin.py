from django.contrib import admin

from .models import Recipe, Ingredient, Tag, IngredientsValue


# class IngredientInline(admin.StackedInline):
#     model = Ingredient
#     filter_horizontal = ()

class IngredientsValueInline(admin.TabularInline):
    model = IngredientsValue
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('pk', 'title', 'slug')
    list_filter = ('title', 'slug')
    empty_value_display = '-empty-'
    inlines = [IngredientsValueInline,]

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'unit', )
    search_fields = ('ingredient', )
    list_filter = ('ingredient', )
    empty_value_display = '-empty-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag', )
    search_fields = ('tag', )
    list_filter = ('tag',)
    empty_value_display = '-empty-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)