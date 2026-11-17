from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .google import GoogleLoginAPIView
from .views import CustomTokenObtainPairView, MeView, RegisterView


app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("google/login/", GoogleLoginAPIView.as_view(), name="google-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", MeView.as_view(), name="me"),
]
