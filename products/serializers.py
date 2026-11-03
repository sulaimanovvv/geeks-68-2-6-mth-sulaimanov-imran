from rest_framework import serializers

from common.validators import validate_product_creator_age

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "owner",
            "title",
            "description",
            "price",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "owner", "created_at", "updated_at")

    def validate(self, attrs):
        request = self.context.get("request")
        if request is not None and request.method == "POST":
            validate_product_creator_age(request)
        return attrs
