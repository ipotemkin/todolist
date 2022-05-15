from django.db import models

from core.models import User


class TgUser(models.Model):
    chat_id = models.PositiveBigIntegerField(verbose_name="Telegram chat_id", unique=True)
    username = models.CharField(
        verbose_name="Telegram user_ud",
        max_length=255,
        null=True,
        blank=True,
        default=None
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None
    )
    verification_code = models.CharField(
        verbose_name="Код подтверждения",
        max_length=50, null=True, blank=True, default=None
    )

    def __str__(self):
        if self.username:
            return self.username
        elif self.user and self.username:
            return self.user.username
        else:
            return super().__str__()

    class Meta:
        verbose_name = "Пользователь Телеграм"
        verbose_name_plural = "Пользователи Телеграм"
