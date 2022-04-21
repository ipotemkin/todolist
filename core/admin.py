from django.contrib import admin
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.admin import UserAdmin

from core.models import User

# class UserAdmin gives a possibility to change the user's password


@admin.register(User)
# class BoardAdmin(admin.ModelAdmin):
class BoardAdmin(UserAdmin):

    # exclude = ('password',)

    readonly_fields = ('date_joined', 'last_login')
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'last_login')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ("Логин и пароль", {"fields": ("username", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name", "email")}),
        ("Права доступа", {"fields": ("role", "is_active")}),
        (None, {"fields": ("date_joined", "last_login")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2")}),
        ("Персональная информация", {"fields": ("first_name", "last_name", "email")}),
        ("Права доступа", {"fields": ("role", "is_active")}),
    )
    admin.site.unregister(BaseGroup)
