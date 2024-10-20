from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите email"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Выберите аватар",
        null=True,
        blank=True,
    )
    telegram_chat_id = models.CharField(
        max_length=35,
        verbose_name="ID чата Telegram",
        help_text="Укажите ID чата Telegram",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
