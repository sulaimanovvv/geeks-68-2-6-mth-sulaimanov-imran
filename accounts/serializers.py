from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "birthdate",
            "is_staff",
        )
        read_only_fields = ("id", "email", "is_staff")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone_number",
            "birthdate",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "phone_number": {"required": False, "allow_blank": True},
            "birthdate": {"required": False, "allow_null": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Пароли не совпадают."}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        return CustomUser.objects.create_user(password=password, **validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthdate"] = user.birthdate.isoformat() if user.birthdate else None
        return token
