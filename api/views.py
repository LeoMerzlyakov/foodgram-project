from recipes.models import Favorite, Recipe
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from django.shortcuts import get_object_or_404

from .serializers import FavoriteSerializer
from .service import get_ingredients


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
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


    def destroy(self, request, recipe=None):
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        favor_note = get_object_or_404(
            Favorite,
            recipe=serializer.validated_data['recipe'],
            user = request.user
        )
        favor_note.delete()
        return Response(data='delete success')
