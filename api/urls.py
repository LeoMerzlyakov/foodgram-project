from django.urls import include, path

from .views import FavoriteViewSet, ingredients_found, PurchasesViewSet
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('purchases', PurchasesViewSet, basename='purchases')
    
urlpatterns = [
    path('', include(router.urls)),
    path('ingredients', ingredients_found),
]