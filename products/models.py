from django.conf import settings
from django.db import models


class Product(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="владелец",
    )
    title = models.CharField("название", max_length=255)
    description = models.TextField("описание", blank=True)
    price = models.DecimalField("цена", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("создан", auto_now_add=True)
    updated_at = models.DateTimeField("изменён", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    def __str__(self):
        return self.title
