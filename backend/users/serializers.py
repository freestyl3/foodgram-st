from rest_framework import serializers
from djoser.serializers import UserSerializer

from django.contrib.auth import get_user_model
from .models import Subscription

class FoodgramUserSerializer(UserSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    # is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=obj,
            follower=user
        ).exists()

    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = (
            'email', 'id', 'username', 
            'first_name', 'last_name', 'avatar'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('__all__')