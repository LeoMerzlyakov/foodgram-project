from django.urls import include, path

from .views import FavoriteViewSet, ingredients_found
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('favorites', FavoriteViewSet, basename='favorites')
    
urlpatterns = [
    path('', include(router.urls)),
    path('ingredients', ingredients_found),
]