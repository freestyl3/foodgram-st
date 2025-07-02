from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from .filters import IngredientSearchFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.paginator import RecipePaginator
from django_filters.rest_framework import DjangoFilterBackend

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

    @action(
        methods=['GET'],
        detail=True,
        url_path='get-link',
        permission_classes=(permissions.IsAuthenticatedOrReadOnly, )
    )
    def get_link(self, request, pk):
        short_link = request.build_absolute_uri()[:-9]

        return Response({'short-link': short_link}, status=status.HTTP_200_OK)