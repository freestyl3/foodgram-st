import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.serializers import FoodgramUserSerializer
from .constraints import (
    MIN_COOKING_TIME, MAX_COOKING_TIME,
    MIN_INGREDIENT_AMOUNT, MAX_INGREDIENT_AMOUNT
)
from .models import Ingredient, Recipe, RecipeIngredient


class Base64RecipeField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='recipe.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')
        read_only_fields = ('id', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField(
        min_value=MIN_INGREDIENT_AMOUNT,
        max_value=MAX_INGREDIENT_AMOUNT
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = FoodgramUserSerializer(read_only=True)
    image = Base64RecipeField(required=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredient_amount',
        many=True
    )
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'image', 'text', 'cooking_time',
            'ingredients', 'is_favorited', 'is_in_shopping_cart'
        )
        read_only_fields = ('id', 'author')

    def recipe_ingredient_bulk_create(self, instance, recipe_data):
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=recipe_ingredient['ingredient'],
                    amount=recipe_ingredient['amount']
                ) for recipe_ingredient in recipe_data
            ]
        )

    def create(self, validated_data):
        recipe_data = validated_data.pop('ingredient_amount')
        recipe = Recipe.objects.create(**validated_data)
        self.recipe_ingredient_bulk_create(recipe, recipe_data)
        return recipe

    def update(self, instance, validated_data):
        recipe_data = validated_data.pop('ingredient_amount', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if recipe_data is not None:
            instance.ingredient_amount.all().delete()
            self.recipe_ingredient_bulk_create(instance, recipe_data)
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')

        if not ingredients:
            raise serializers.ValidationError(
                'Recipe must have at least 1 ingredient'
            )

        ingredients_set = set(key['id'] for key in ingredients)

        if len(ingredients) != len(ingredients_set):
            raise serializers.ValidationError(
                'Recipe must have unique ingredients'
            )

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url
        return representation

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return obj.favorited_recipes.filter(user=user.id).exists()
        # return Favorite.objects.filter(
        #     user=user.id,
        #     recipe=obj
        # ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return obj.recipes_in_shopping_cart.filter(user=user.id).exists()
        # return ShoppingCart.objects.filter(
        #     user=user.id,
        #     recipe=obj
        # ).exists()
