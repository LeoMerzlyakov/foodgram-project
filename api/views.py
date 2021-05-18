from django.shortcuts import get_object_or_404

from recipes.models import Favorite, Follow, Purchase

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
from .service import get_ingredients


@api_view(['GET'])
def ingredients_found(request):
    """
    A function for seasrch the ingredients for drop-down list.
    """
    if request.GET['query']:
        find_text = request.GET['query']
        data = get_ingredients(find_text)
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
    return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'success': False}
        )


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    A ModelViewSet for create or delete favorites records.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, instance):
        instance.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Favorite, user=request.user, recipe=kwargs['pk']
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchasesViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    A ViewSet for create or delete purchases records.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        # в запросе приходит параметр 'id' вместо 'recipe'.
        # Добавляю в данные параметр.
        data = request.data
        if request.data['id']:
            data['recipe'] = request.data['id']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, instance):
        instance.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # в запросе приходит параметр 'pk' вместо 'recipe'.
        # Добавляю в данные параметр.
        instance = get_object_or_404(
            Purchase, user=request.user, recipe=kwargs['pk']
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    A ModelViewSet for create or delete Subscription.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Follow.objects.all()
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        # В запросе приходит параметр 'author'. Приходит под именем 'id'.
        # Параметр может придти как 'pk', так и 'username'
        if request.data['id']:
            param = request.data['id']
            try:
                param = int(param)
            except ValueError:
                param = param

            if type(param) == int:
                author = get_object_or_404(User, pk=int(param))
            else:
                author = get_object_or_404(User, username=param)
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

    def destroy(self, request, *args, **kwargs):
        # в запросе приходит параметр 'author' приходит под именеи 'pk'.
        # Параметр может придти как 'pk', так и 'username'
        if kwargs['pk']:
            try:
                param = int(kwargs['pk'])
            except ValueError:
                param = kwargs['pk']

            if type(param) == int:
                author = get_object_or_404(User, pk=int(kwargs['pk']))
            else:
                author = get_object_or_404(User, username=kwargs['pk'])
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
