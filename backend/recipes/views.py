from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.paginator import RecipePaginator
from api.permissions import IsAuthorOrReadOnly
from users.serializers import UserRecipeSerializer

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart)
from .serializers import IngredientSerializer, RecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name', )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = RecipePaginator
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def recipes_management(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            if model.objects.filter(
                    recipe=recipe,
                    user=request.user
                ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            favorite = model.objects.create(
                recipe=recipe,
                user=request.user
            )
            serializer = UserRecipeSerializer(
                recipe, 
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        favorite = model.objects.filter(
            recipe=recipe,
            user=request.user
        )

        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=True,
        url_path='get-link',
        permission_classes=(permissions.IsAuthenticatedOrReadOnly, )
    )
    def get_link(self, request, pk):
        short_link = request.build_absolute_uri()[:-9]

        return Response({'short-link': short_link}, status=status.HTTP_200_OK)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite'
    )
    def favorite(self, request, pk):
        return self.recipes_management(Favorite, request, pk)
    
    @action(
        methods = ['post', 'delete'],
        detail=True,
        url_path='shopping_cart'
    )
    def shopping_cart(self, request, pk):
        return self.recipes_management(ShoppingCart, request, pk)
    
    @action(
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        recipes_in_cart = Recipe.objects.filter(
            recipes_in_shopping_cart__user=request.user
        )

        ingredients = RecipeIngredient.objects.filter(
            recipe__in=recipes_in_cart
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            total=Sum('amount')
        ).order_by('ingredient__name')

        result_list = []

        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            amount = ingredient['total']
            measurement_unit = ingredient['ingredient__measurement_unit']
            result_list.append(f'{name} - {amount} {measurement_unit}')

        result_string = ',\n'.join(result_list)

        return FileResponse(
            result_string, 
            status=status.HTTP_200_OK, 
            as_attachment=True, 
            filename='shopping_list.txt'
        )
