from rest_framework import viewsets, permissions, serializers, status
from djoser.views import UserViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from .serializers import FoodgramUserSerializer, SubscriptionSerializer
from .models import Subscription

class FoodgramUserViewSet(UserViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = FoodgramUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (permissions.IsAuthenticatedOrReadOnly(), )
        return super().get_permissions()
    
    @action(
        methods=['post', 'delete'],
        url_path='subscribe',
        permission_classes=(permissions.IsAuthenticated, ),
        detail=True
    )
    def subscribe(self, request, id):
        follower = request.user
        following_user = get_object_or_404(
            get_user_model(),
            id=id
        )
        if request.method == 'POST':

            if (
                follower == following_user or 
                Subscription.objects.filter(
                    user=following_user,
                    follower=follower
                ).exists()
            ):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            subscription = Subscription.objects.create(
                user=following_user,
                follower=follower
            )

            serializer = SubscriptionSerializer(
                subscription.user,
                context={'request': request}
            )

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )