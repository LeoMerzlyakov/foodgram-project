from django.urls import path

from . import views


app_name = 'recipes'
urlpatterns = [
    path(
        '',
        views.recipes,
        name='recipes'
    ),
    path(
        'recipes/author/<int:user_id>/',
        views.user_recipes,
        name='recipes_by_author'
    ),
    path(
        'recipes/<int:recipe_id>/',
        views.recipe,
        name='recipe'
    ),
    path(
        'recipes/delete/<int:recipe_id>/',
        views.delete_recipe,
        name='delete_recipe'
    ),
    path(
        'recipes/<int:recipe_id>/edit/',
        views.edit_recipes,
        name='recipe_edit'
    ),
    path(
        'recipes/new/',
        views.create_recipe,
        name='recipe_new'
    ),
    path(
        'favorites/',
        views.favorites,
        name='favorites'
    ),
    path(
        'follows/',
        views.follows,
        name='my_follows'
    ),
    path(
        'purchases/', views.purchases, name='purchases'
    ),
    path(
        'purchases/delete/<int:recipe_id>/',
        views.purchases_delete,
        name='purchases_delete'
    ),
    path(
        'purchases/export_pdf/',
        views.export_pdf,
        name='export_pdf'
    ),
    path('pages/<str:page>', views.other_page, name='other'),
]

