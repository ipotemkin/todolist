from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id',)
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )


class CreateUserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat'
        )

    def validate(self, attrs: dict) -> dict:
        password: str = attrs.get('password')
        password_repeat: str = attrs.pop('password_repeat', None)
        if password != password_repeat:
            raise ValidationError('passwords are not equal')
        return attrs

    def create(self, validated_data) -> User:
        return User.objects.create_user(**validated_data)


# to correctly show a response model in swagger
class LoginResponseSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class LoginSerializer(LoginResponseSerializer):
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> User:
        if user := authenticate(**attrs):
            return user
        raise AuthenticationFailed

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        read_only_fields = ('id',)
        fields = ('old_password', 'new_password')

    def validate(self, attrs: dict) -> dict:
        old_password = attrs.get('old_password')
        user: User = self.instance
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'fields is incorrect'})
        return attrs

    def update(self, instance: User, validated_data) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance
