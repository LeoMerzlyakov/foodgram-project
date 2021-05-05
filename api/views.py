from django.core.checks import messages
from recipes.models import Favorite, Purchase
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from django.shortcuts import get_object_or_404
from django.db import InternalError

from .serializers import FavoriteSerializer, PurchseSerializer
from .service import get_ingredients, get_favor_note


@api_view(['GET'])
def ingredients_found(request):
    """
    A function for seasrch the ingredients for drop-down list.
    """
    find_text =  request.GET['query']
    data = get_ingredients(find_text)
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )


class FavoriteViewSet(viewsets.ViewSet):
    """
    A ViewSet for create or delete favorites records.
    """
    def create(self, request):
        data=request.data
        data['user'] = request.user
        serializer = FavoriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        user = request.user
        instance = get_object_or_404(Favorite, recipe=pk, user=user)
        try:
            instance.delete()
        except InternalError:
            error_msg = {'error': 'InternalError message'}
            raise InternalError(error_msg)
        return Response(status=status.HTTP_204_NO_CONTENT, data={"success": True})


class PurchasesViewSet(viewsets.ViewSet):
    """
    A ViewSet for create or delete purchases records.
    """
    def create(self, request):
        data=request.data
        data['recipe'] = request.data['id']
        serializer = PurchseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        user = request.user
        instance = get_object_or_404(Purchase, recipe=pk, user=user)
        try:
            instance.delete()
        except InternalError:
            error_msg = {'error': 'InternalError message'}
            raise InternalError(error_msg)
        return Response(status=status.HTTP_204_NO_CONTENT, data={"success": True})
