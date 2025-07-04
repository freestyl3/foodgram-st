from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Subscription


@admin.register(get_user_model())
class FoogramUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('avatar',)}),
    )
    search_fields = ('username', 'email')
    list_filter = ('is_staff', )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_filter = ()
    search_fields = ('user__username', 'follower__username')
