from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from core import views
from todolist.settings import DJANGO_LOGIN_LOGOUT_DRF

app_name = 'core'

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view()),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('update_password', views.UpdatePasswordView.as_view(), name='change-password'),
]

if DJANGO_LOGIN_LOGOUT_DRF:
    urlpatterns += [
        # to django logout via swagger ui + DRF
        path('login', views.LoginView.as_view(), name='login'),
        path('logout', views.LogoutView.as_view(), name='logout'),
    ]
else:
    urlpatterns += [
        # django login/logout to work in swagger ui
        path('django-login', LoginView.as_view(), name='login'),
        path('logout', LogoutView.as_view(), name='logout'),
    ]
