from rest_framework import serializers
from recipes.models import Favorite, Recipe
from django.db import IntegrityError


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorities model"""

    class Meta:
            model = Favorite
            fields = '__all__'
            read_only_fields = ['user']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            error_msg = {'error': 'IntegrityError message'}
            raise serializers.ValidationError(error_msg)
