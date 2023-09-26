from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """User's custom model."""
    email = models.EmailField(
        verbose_name="Email", max_length=254, unique=True, blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Пользователь: {self.email}"
