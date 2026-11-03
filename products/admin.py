from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "owner", "created_at")
    search_fields = ("title", "owner__email")
    list_filter = ("created_at",)
