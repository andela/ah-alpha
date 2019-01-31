"""
Django settings for authors project.

Generated by 'django-admin startproject' using Django 2.1.4.14.

For more information on this file, see
https://docs.djangoproject.com/en/2.1.4/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1.4/ref/settings/
"""

import os
import django_heroku
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1.4/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7pgozr2jn7zs_o%i8id6=rddie!*0f0qy3$oy$(8231i^4*@u3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Email config
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = os.getenv("DEAFULT_FROM_EMAIL")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'taggit',
    'cloudinary',

    'authors.apps.authentication',
    'authors.apps.articles',
    'authors.apps.rating',

    'authors.apps.like_dislike',
    'authors.apps.core',
    'authors.apps.comments',
    'authors.apps.profiles',
    'authors.apps.reading_stats',
    'rest_framework_swagger',
    # credits --> https://github.com/axnsan12/drf-yasg
    'drf_yasg',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'authors.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'authors.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1.4/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'PORT': os.getenv('DB_PORT'),
        'HOST': os.getenv('DB_HOST')

    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1.4/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1.4/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = (
    '0.0.0.0:4000',
    'localhost:4000',
)

# Tell Django about the custom `User` model we created. The string
# `authentication.User` tells Django we are referring to the `User` model in
# the `authentication` module. This module is registered above in a setting
# called `INSTALLED_APPS`.
AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'authors.apps.core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Django Rest Framework Jwt settings
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

        'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

        'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

        'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

        'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

        'JWT_SECRET_KEY': SECRET_KEY,
        'JWT_GET_USER_SECRET_KEY': None,
        'JWT_PUBLIC_KEY': None,
        'JWT_PRIVATE_KEY': None,
        'JWT_ALGORITHM': 'HS256',
        'JWT_VERIFY': True,
        'JWT_VERIFY_EXPIRATION': True,
        'JWT_LEEWAY': 0,
        'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=3),
        'JWT_AUDIENCE': None,
        'JWT_ISSUER': None,

        'JWT_ALLOW_REFRESH': False,
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=10800),

        'JWT_AUTH_HEADER_PREFIX': 'Bearer',
        'JWT_AUTH_COOKIE': None,

}

CLOUDINARY = {
    'cloud_name': os.getenv('CLOUDINARY_NAME'),
    'api_key': os.getenv('CLOUDINARY_KEY'),
    'api_secret': os.getenv('CLOUDINARY_SECRET'),
    'secure': True
}

# Activate Django-Heroku.
django_heroku.settings(locals())

# Swagger settings

SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'USE_SESSION_AUTH': False,
    'DOC_EXPANSION': 'list',
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'JSON_EDITOR': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'REFETCH_SCHEMA_ON_LOGOUT': True,
    'DEFAULT_MODEL_RENDERING': 'example',

}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
# facebook authentication credentials
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FB_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FB_SECRET')

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    "fields": "id, email, name"
}
# google authentication credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_SECRET')
SOCIAL_AUTH_GOOGLE_SCOPE = ['email', 'username', 'password']

# twitter authentication credentials
SOCIAL_AUTH_TWITTER_KEY = os.getenv('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.getenv('TWITTER_SECRET')
SOCIAL_AUTH_TWITTER_SCOPE = ['email']
