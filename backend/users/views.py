from rest_framework import viewsets, permissions, serializers, status
from djoser.views import UserViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import FoodgramUserSerializer, SubscriptionSerializer
from .models import Subscription
from api.paginator import FoodgramUserPaginator

class FoodgramUserViewSet(UserViewSet):
    queryset = get_user_model().objects.all()
    pagination_class = FoodgramUserPaginator
    serializer_class = FoodgramUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (permissions.IsAuthenticatedOrReadOnly(), )
        return super().get_permissions()
    
    def get_serializer_class(self):
        '''Для правильного отображения полей 
        при запросе на эндпоинт users/me/
        '''
        if self.action == 'me':
            return FoodgramUserSerializer
        return super().get_serializer_class()
    
    @action(
        methods=['post', 'delete'],
        url_path='subscribe',
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
        
        subscription = Subscription.objects.filter(
            user=following_user,
            follower=follower
        )

        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

        
    @action(
        methods=['get', ],
        url_path='subscriptions',
        detail=False,
    )
    def subscriptions(self, request):
        paginator = self.pagination_class()

        subscriptions = get_user_model().objects.filter(
            subscriptions__follower=request.user.id
        )

        page = paginator.paginate_queryset(
            subscriptions,
            request=request
        )
        
        serializer = SubscriptionSerializer(
            page, many=True, 
            context={'request':request}
        )

        return paginator.get_paginated_response(serializer.data)
    
    @action(
        methods=['put', 'delete'],
        detail=False,
        url_path='me/avatar'
    )
    def avatar(self, request):
        user = request.user

        if request.method == 'PUT':

            if 'avatar' not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            serializer = FoodgramUserSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data={'avatar': user.avatar.url},
                status=status.HTTP_200_OK
            )
        
        if user.avatar:
            user.avatar.delete()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
