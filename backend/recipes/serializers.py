import base64

from rest_framework import serializers
from django.core.files.base import ContentFile
from django.db import transaction

from .models import Ingredient, Recipe, RecipeIngredient, Favorite, ShoppingCart
from users.serializers import FoodgramUserSerializer


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
        queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
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

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'cooking_time', 'ingredients', 'is_favorited', 'is_in_shopping_cart')
        read_only_fields = ('id', 'author')

    def create(self, validated_data):
        recipe_data = validated_data.pop('ingredient_amount')
        recipe = Recipe.objects.create(**validated_data)
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=recipe_ingredient['id'],
                    amount=recipe_ingredient['amount']
                ) for recipe_ingredient in recipe_data
            ]
        )
        return recipe
    
    def update(self, instance, validated_data):
        print(validated_data)
        recipe_data = validated_data.pop('ingredient_amount', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if recipe_data is not None:
            instance.ingredient_amount.all().delete()
            RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=recipe_ingredient['id'],
                    amount=recipe_ingredient['amount']
                ) for recipe_ingredient in recipe_data
            ]
        )
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
        user = self.context.get('request').user
        return Favorite.objects.filter(
            user=user.id,
            recipe=obj
        ).exists()
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return ShoppingCart.objects.filter(
            user=user.id,
            recipe=obj
        ).exists()
