from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('avatar',)}),
    )
    search_fields = ('username', 'email')
    list_filter = ('is_staff', )
# Register your models here.
