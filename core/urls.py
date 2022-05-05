from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view()),  # name='login'),  # commented not to work via swagger
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('update_password', views.UpdatePasswordView.as_view(), name='change-password'),

    # TODO remove
    # path('logout', views.LogoutView.as_view(), name='logout'),

    # django login/logout to work in swagger ui
    path('django-login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
