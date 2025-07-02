from django.contrib import admin

from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_filter = ()
# Register your models here.
