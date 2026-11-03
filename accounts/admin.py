from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ("email",)
    list_display = ("email", "phone_number", "birthdate", "is_staff", "is_active")
    search_fields = ("email", "phone_number")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личные данные", {"fields": ("first_name", "last_name", "phone_number", "birthdate")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("date_joined", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "birthdate",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
