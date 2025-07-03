import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Recipe

from .models import FoodgramUser, Subscription


class Base64AvatarField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='avatar.' + ext)

        return super().to_internal_value(data)


class FoodgramUserSerializer(UserSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64AvatarField(required=False, allow_null=True)

    class Meta(UserSerializer.Meta):
        model = FoodgramUser
        fields = (
            'email', 'id', 'username', 'is_subscribed',
            'first_name', 'last_name', 'avatar'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=obj,
            follower=user
        ).exists()

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None


class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'id', 'username', 'is_subscribed', 'recipes',
            'first_name', 'last_name', 'avatar', 'recipes_count'
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.all()

        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = None

        if limit:
            recipes = recipes[:limit]

        return UserRecipeSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
