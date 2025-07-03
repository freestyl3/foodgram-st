from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class Recipe(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='ingredients'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(limit_value=1), ]
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created_at', )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=128,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Игредиенты'
        ordering = ('name', )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_amount'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(limit_value=1), ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        amount = self.amount
        name = self.ingredient.name
        measurement_unit = self.ingredient.measurement_unit
        recipe_name = self.recipe.name
        return f'{amount} {measurement_unit} {name} в {recipe_name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorited_recipes'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('recipe', )

    def __str__(self):
        recipe_name = self.recipe.name
        username = self.user.username
        return f'{recipe_name} в избранном у {username}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipes_in_shopping_cart'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ('-created_at', )

    def __str__(self):
        recipe_name = self.recipe.name
        username = self.user.username
        return f'{recipe_name} в корзине у {username}'
