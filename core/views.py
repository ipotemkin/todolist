# from django.shortcuts import render
from django.contrib.auth import login, logout
from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView
)
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from core.models import User
from core.serializers import (
    CreateUserSerializer,
    LoginSerializer,
    UserSerializer,
    UpdatePasswordSerializer
)


def login_model_backend(request, user) -> None:
    login(
        request,
        user=user,
        backend='django.contrib.auth.backends.ModelBackend'
    )


# @ensure_csrf_cookie
class SignupView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        ret = super().post(request, *args, **kwargs)

        # to log in the app; the front doesn't do it! ((
        user = User.objects.get(username=ret.data['username'])
        login_model_backend(request, user=user)

        return ret


# @ensure_csrf_cookie
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    # @csrf_exempt
    # @ensure_csrf_cookie
    def post(self, request, *args, **kwargs) -> Response:
        user_login: LoginSerializer = self.get_serializer(data=request.data)
        user_login.is_valid(raise_exception=True)
        username = user_login.validated_data['username']
        user = User.objects.get(username=username)
        login_model_backend(request, user=user)
        user_serializer = UserSerializer(instance=user)
        return Response(user_serializer.data)


# @ensure_csrf_cookie
class ProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    # @csrf_exempt
    def get_object(self) -> User:
        return self.request.user

    # @csrf_exempt
    def delete(self, request, *args, **kwargs) -> Response:
        logout(request)
        return Response({})

    # @csrf_exempt
    # @ensure_csrf_cookie
    # def destroy(self, request, *args, **kwargs) -> Response:
    #     logout(request)
    #     return Response({})


class UpdatePasswordView(UpdateAPIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    # @csrf_exempt
    def get_object(self) -> User:
        return self.request.user

    # @csrf_exempt
    def update(self, request, *args, **kwargs) -> Response:
        ret = super().update(request, *args, **kwargs)

        # to keep the current user logged in
        login_model_backend(request, user=request.user)

        return ret
