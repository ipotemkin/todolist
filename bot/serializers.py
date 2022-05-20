from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)
    tg_id = serializers.SlugField(source="chat_id", read_only=True)

    class Meta:
        model = TgUser
        fields = ("tg_id", "username", "verification_code", "user_id")
        read_only_fields = ("tg_id", "username", "user_id")

    def validate(self, attrs):
        verification_code = attrs.pop("verification_code")
        tg_user_name = cache.get(verification_code)

        if tg_user_name and (
            tg_user := TgUser.objects.filter(username=tg_user_name).first()
        ):
            attrs["tg_user"] = tg_user
            return attrs

        raise ValidationError({"verification_code": "field is incorrect"})
