from django.core.cache import cache
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Product
from .permissions import CanCreateProduct, IsOwnerOrModerator
from .serializers import ProductSerializer


@extend_schema_view(
    list=extend_schema(tags=["Продукты"], summary="Список продуктов"),
    retrieve=extend_schema(tags=["Продукты"], summary="Один продукт"),
    create=extend_schema(tags=["Продукты"], summary="Создать продукт (только 18+)"),
    update=extend_schema(tags=["Продукты"], summary="Полностью изменить продукт"),
    partial_update=extend_schema(tags=["Продукты"], summary="Частично изменить продукт"),
    destroy=extend_schema(tags=["Продукты"], summary="Удалить продукт"),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("owner").all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cached_products = cache.get("products")

        if cached_products:
            print("redis")
            return Response(cached_products)

        response = super().list(request, *args, **kwargs)

        if response.data:
            cache.set("products", response.data, timeout=300)

        print("database")
        return response

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            permission_classes = (AllowAny,)
        elif self.action == "create":
            permission_classes = (CanCreateProduct,)
        else:
            permission_classes = (IsOwnerOrModerator,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
