from django.contrib.auth import authenticate, logout
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        read_only_fields = ('id',)
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('username or password is incorrect')
        return attrs

    # def update(self, instance, validated_data):
    #     pass
    #
    # def create(self, validated_data):
    #     pass


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
