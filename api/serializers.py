from rest_framework import serializers
from recipes.models import Favorite, Purchase, Recipe, Follow
from rest_framework.validators import UniqueTogetherValidator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from users.models import User


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


class PurchseSerializer(serializers.ModelSerializer):
    """Serializer for Purchase model"""

    class Meta:
            model = Purchase
            fields = '__all__'
            read_only_fields = ['user']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            error_msg = {'error': 'IntegrityError message'}
            raise serializers.ValidationError(error_msg)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Follow model"""

    class Meta:
        model = Follow
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Подписка уже оформлена' 
            )
        ]

