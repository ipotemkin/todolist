from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLES = ((USER, "Пользователь"), (ADMIN, "Администратор"))

    role = models.CharField(max_length=5, choices=ROLES, default=USER, verbose_name="Роль")
