from rest_framework import viewsets, permissions, serializers
from djoser.views import UserViewSet

from django.contrib.auth import get_user_model
from .serializers import FoodgramUserSerializer

class FoodgramUserViewSet(UserViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = FoodgramUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (permissions.IsAuthenticatedOrReadOnly(), )
        return super().get_permissions()
    
