from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class CustomUser(AbstractUser):
    """User's custom model."""
    email = models.EmailField(
        verbose_name="Почтовый адрес",
        max_length=254,
        unique=True,
        blank=False,
    )
    username = None
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Пользователь: {self.email}"

    class Meta:
        verbose_name = "Пользователь"
