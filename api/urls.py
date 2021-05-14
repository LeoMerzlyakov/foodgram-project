from django.urls import include, path

from rest_framework import routers

from .views import (
    FavoriteViewSet,
    PurchasesViewSet,
    SubscriptionViewSet,
    ingredients_found,
)


app_name = 'api'

router = routers.DefaultRouter()
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('purchases', PurchasesViewSet, basename='purchases')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('ingredients', ingredients_found),
]
