from django.db import models
from django.contrib.auth import get_user_model


class Recipe(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    # string url
    image = models.ImageField(
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='ingredients'
    )
    # is_favourited
    # is_in_shopping_cart
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ('name', )


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=128
    )
    measurment_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64
    )

    class Meta:
        verbose_name = 'Ингредиент'
        ordering = ('name', )
    

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, 
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )