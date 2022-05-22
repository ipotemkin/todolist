"""
Django settings for todolist project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, False),
    SOCIAL_AUTH_VK_OAUTH2_KEY=(str, "example"),
    SOCIAL_AUTH_VK_OAUTH2_SECRET=(str, "example"),
    NO_FRONT=(bool, False),
    REDIS_HOST=(str, "localhost"),
    BOT_TOKEN=(str, "testing-bot-token"),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

DJANGO_LOGIN_LOGOUT_DRF = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

NO_FRONT = env("NO_FRONT")

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = (
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8002",
    "http://127.0.0.1:8002",
    "http://0.0.0.0:8002",
    "http://51.250.72.80:8002",
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "social_django",
    "corsheaders",
    "django_filters",
    "core",
    "goals",
    "bot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "todolist.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "todolist.wsgi.application"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.vk.VKOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# Social auth
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_VK_OAUTH2_KEY = env("SOCIAL_AUTH_VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = env("SOCIAL_AUTH_VK_OAUTH2_SECRET")
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ["email"]  # , 'photos', 'notify']
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"  # '/logged-in/'
SOCIAL_AUTH_LOGIN_ERROR_URL = "/login-error/"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# DATABASES = {'default': env.db('DATABASE_URL')}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# to modify the system user class
AUTH_USER_MODEL = "core.User"

# for 'social_django' to work without a trailing slash
SOCIAL_AUTH_TRAILING_SLASH = False

APPEND_SLASH = False

# чтобы возвращатьяся в Swagger после Django Login/Logout, но это не работает ((
# помогает только нажатие на ссылку Schema
LOGOUT_REDIRECT_URL = "core/" if NO_FRONT else "swagger/core/"

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
    },
    # 'USE_SESSION_AUTH': False,  # отключает Django Login/Logout в Swagger
    # django login/logout via SWAGGER UI+DRF or Django default + my login.html
    "LOGIN_URL": "rest_framework:login" if DJANGO_LOGIN_LOGOUT_DRF else "core:login",
    "LOGOUT_URL": "rest_framework:logout" if DJANGO_LOGIN_LOGOUT_DRF else "core:logout",
    "LOGIN_REDIRECT_URL": "/",
    "LOGOUT_REDIRECT_URL": LOGOUT_REDIRECT_URL,
}

BOT_TOKEN = env.str("BOT_TOKEN")

REDIS_HOST = env.str("REDIS_HOST")

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": f"{REDIS_HOST}:6379",
    },
}


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }
