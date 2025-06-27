from rest_framework import serializers
from djoser.serializers import UserSerializer

from django.contrib.auth import get_user_model

class FoodgramUserSerializer(UserSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = (
            'email', 'id', 'username', 
            'first_name', 'last_name', 'avatar'
        )