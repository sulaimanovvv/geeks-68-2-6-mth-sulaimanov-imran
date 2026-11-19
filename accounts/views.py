from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ConfirmRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @extend_schema(tags=["Авторизация"], summary="Регистрация по email")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ConfirmRegistrationView(generics.GenericAPIView):
    serializer_class = ConfirmRegistrationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(tags=["Авторизация"], summary="Подтверждение регистрации")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Регистрация подтверждена."})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(tags=["Авторизация"], summary="Вход по email и получение JWT")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @extend_schema(tags=["Пользователь"], summary="Текущий пользователь")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["Пользователь"], summary="Изменить профиль")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
