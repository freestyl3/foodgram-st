from rest_framework import serializers

from django.contrib.auth import get_user_model

class FoodgramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'avatar')