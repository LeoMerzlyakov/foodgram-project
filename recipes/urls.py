from django.urls import include, path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('recipes/author/<int:user_id>/', views.user_recipes, name='recipes_by_author'),
    path('recipes/<int:recipe_id>/', views.recipe, name='recipe'),
    path('recipes/<int:recipe_id>/edit/', views.edit_recipes, name='recipe_edit'),
    path('recipes/new/', views.create_recipe, name='recipe_new'),
    path('favorites/', views.favorites, name='favorites'),
    path('follows/', views.follows, name='my_follows'),
    path('purchases/', views.purchases, name='purchases'),
]