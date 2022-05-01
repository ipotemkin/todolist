from django.contrib.auth import login, logout
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView, DestroyAPIView, RetrieveAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.models import User
from core.serializers import (
    CreateUserSerializer,
    LoginSerializer,
    UserSerializer,
    UpdatePasswordSerializer, LoginResponseSerializer
)


def login_model_backend(request, user) -> None:
    login(
        request=request,
        user=user,
        backend='django.contrib.auth.backends.ModelBackend'
    )


class SignupView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        ret = super().post(request, *args, **kwargs)

        # to log in the app; the front doesn't do it! ((
        user = User.objects.get(username=ret.data['username'])
        login_model_backend(request, user=user)

        return ret


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(responses={200: LoginResponseSerializer()})
    def post(self, request, *args, **kwargs) -> Response:
        user_login = self.get_serializer(data=request.data)
        user_login.is_valid(raise_exception=True)

        # username = user_login.validated_data['username']
        # user = User.objects.get(username=username)
        # login_model_backend(request, user=user)
        # user_serializer = UserSerializer(instance=user)
        # return Response(user_serializer.data)

        login_model_backend(request=request, user=user_login.validated_data)
        return Response(user_login.data, status=200)


class UserMixin(GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user


class ProfileView(RetrieveUpdateDestroyAPIView, UserMixin):
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs) -> Response:
        logout(request)
        return Response({})


class LogoutView(RetrieveAPIView, UserMixin):
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs) -> Response:
        logout(request)
        return Response({"message": "user logged out"}, status=200)


class UpdatePasswordView(UpdateAPIView, UserMixin):
    serializer_class = UpdatePasswordSerializer

    def update(self, request, *args, **kwargs) -> Response:
        ret = super().update(request, *args, **kwargs)

        # to keep the current user logged in
        login_model_backend(request, user=request.user)

        return ret
