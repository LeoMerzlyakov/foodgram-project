from rest_framework import serializers
from recipes.models import Favorite, Recipe


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorities model"""

    class Meta:
            model = Favorite
            fields = '__all__'
            read_only_fields = ['user']
