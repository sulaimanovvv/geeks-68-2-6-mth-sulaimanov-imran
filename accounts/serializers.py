import secrets

from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


CONFIRMATION_CODE_TIMEOUT = 300


def get_confirmation_code_key(email):
    return f"confirmation_code:{email.lower()}"


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
            "registration_source",
        )
        read_only_fields = ("id", "email", "is_staff", "registration_source")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(read_only=True)

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
            "confirmation_code",
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
        user = CustomUser.objects.create_user(
            password=password,
            is_active=False,
            **validated_data,
        )

        confirmation_code = str(secrets.randbelow(900000) + 100000)
        cache.set(
            get_confirmation_code_key(user.email),
            confirmation_code,
            timeout=CONFIRMATION_CODE_TIMEOUT,
        )

        # Пока отправки по email нет, возвращаем код в ответе для проверки.
        user.confirmation_code = confirmation_code
        return user


class ConfirmRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        email = attrs["email"].lower()
        cache_key = get_confirmation_code_key(email)
        saved_code = cache.get(cache_key)

        if saved_code is None:
            raise serializers.ValidationError(
                {"code": "Код не найден или срок его действия истёк."}
            )

        if saved_code != attrs["code"]:
            raise serializers.ValidationError({"code": "Неверный код."})

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Пользователь не найден."}
            )

        attrs["user"] = user
        attrs["cache_key"] = cache_key
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.is_active = True
        user.save(update_fields=("is_active",))
        cache.delete(self.validated_data["cache_key"])
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthdate"] = user.birthdate.isoformat() if user.birthdate else None
        return token


class GoogleSerializer(serializers.Serializer):
    code = serializers.CharField()
