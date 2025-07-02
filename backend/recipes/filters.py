from rest_framework import filters
import django_filters

from .models import Recipe

class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'

class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter()
    is_in_shopping_cart = django_filters.BooleanFilter()

    class Meta:
        model = Recipe
        fields = ('author', )

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset
    
    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_shopping_cart__user=self.request.user)
        return queryset