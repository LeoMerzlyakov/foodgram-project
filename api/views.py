from django.shortcuts import get_object_or_404

from recipes.models import Favorite, Follow, Purchase, Recipe

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User

from .serializers import (
    FavoriteSerializer,
    PurchaseSerializer,
    SubscriptionSerializer,
)
from .service import get_ingredients, get_author_instance


@api_view(['GET'])
def ingredients_found(request):
    """
    A function for seasrch the ingredients for drop-down list.
    """
    if request.query_params.get('query'):
        data = get_ingredients(request.query_params.get('query'))
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
    return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'success': False}
        )


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]



class FavoriteViewSet(CustomViewSet):
    """
    A ModelViewSet for create or delete favorites records.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, instance):
        instance.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Favorite, user=request.user, recipe=kwargs.get('pk')
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchasesViewSet(CustomViewSet):
    """
    A ViewSet for create or delete purchases records.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, instance):
        recipe = get_object_or_404(Recipe, id=self.request.data.get('id'))
        instance.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Purchase, user=request.user, recipe=kwargs.get('pk')
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(CustomViewSet):
    """
    A ModelViewSet for create or delete Subscription.
    """
    queryset = Follow.objects.all()
    serializer_class = SubscriptionSerializer

    def create_not_used(self, request, *args, **kwargs):
        if request.data.get('id'):
            author = get_author_instance(request.data.get('id'))
            data = {
                'author': author.pk,
                'user': request.user.pk,
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'success': False}
        )

    def perform_create(self, serializer):
        author = get_author_instance(self.request.data.get('id'))
        serializer.save(user=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            author = get_author_instance(kwargs.get('pk'))
            user = request.user
            instance = get_object_or_404(Follow, author=author, user=user)
            self.perform_destroy(instance)
            return Response(
                status=status.HTTP_204_NO_CONTENT, data={"success": True}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'success': False}
        )
