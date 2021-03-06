from django.db import IntegrityError

from recipes.models import Favorite, Follow, Purchase

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


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


class PurchaseSerializer(serializers.ModelSerializer):
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
