from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


phone_number_validator = RegexValidator(
    regex=r"^\+996\d{9}$",
    message="Номер телефона должен быть в формате +996XXXXXXXXX.",
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен.")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError("Пароль обязателен для суперпользователя.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("У суперпользователя is_staff должен быть True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("У суперпользователя is_superuser должен быть True.")
        if not extra_fields.get("phone_number"):
            raise ValueError("Номер телефона обязателен для суперпользователя.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    first_name = models.CharField("имя", max_length=150, blank=True)
    last_name = models.CharField("фамилия", max_length=150, blank=True)
    phone_number = models.CharField(
        "номер телефона",
        max_length=13,
        blank=True,
        validators=[phone_number_validator],
        help_text="Формат: +996XXXXXXXXX",
    )
    birthdate = models.DateField("дата рождения", null=True, blank=True)
    is_staff = models.BooleanField("статус сотрудника", default=False)
    is_active = models.BooleanField("активен", default=True)
    date_joined = models.DateTimeField("дата регистрации", auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ("-date_joined",)

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email).lower()
        if self.is_superuser and not self.phone_number:
            raise ValidationError(
                {"phone_number": "Номер телефона обязателен для суперпользователя."}
            )

    def __str__(self):
        return self.email
