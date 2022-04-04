from django.contrib import admin
from django.contrib.auth.models import Group as BaseGroup

from core.models import User


@admin.register(User)
class BoardAdmin(admin.ModelAdmin):
    exclude = ('password',)
    readonly_fields = ('date_joined', 'last_login')
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {"fields": ("username",)}),
        ("Личная информация", {"fields": ("first_name", "last_name", "email")}),
        ("Разрешения", {"fields": ("role", "is_active")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username",)}),
        ("Личная информация", {"fields": ("first_name", "last_name", "email")}),
        ("Разрешения", {"fields": ("role", "is_active")}),
    )
    admin.site.unregister(BaseGroup)
