# Generated by Django 5.2.3 on 2025-07-02 15:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipeingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1)], verbose_name='Время приготовления'),
        ),
    ]
