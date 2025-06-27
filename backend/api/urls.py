from django.urls import include, path
from rest_framework import routers

from users.views import FoodgramUserViewSet

router = routers.DefaultRouter()
router.register('users', FoodgramUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]