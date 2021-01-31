from django.conf import settings
import os

def pytest_configure():
    settings.configure(
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'rest_framework',
            'channels',

            'board_game.apps.BoardgameConfig',
            ],
        SECRET_KEY="Not_a_secret_key",


        # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),

        # Quick-start development settings - unsuitable for production
        # See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

        # SECURITY WARNING: keep the secret key used in production secret!

        # SECURITY WARNING: don't run with debug turned on in production!

        ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com'],

        # Application definition


        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',
            # 'debug_toolbar.middleware.DebugToolbarMiddleware',
            'request_logging.middleware.LoggingMiddleware',

        ],

        ROOT_URLCONF = 'configuration.urls',


        WSGI_APPLICATION = 'configuration.wsgi.application',
        ASGI_APPLICATION = 'configuration.routing.application',


        # Password validation
        # https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
        ],

        # Internationalization
        # https://docs.djangoproject.com/en/3.0/topics/i18n/
        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.TokenAuthentication',
                'rest_framework.authentication.SessionAuthentication',
            ),
            'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework.permissions.AllowAny',
                # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
                # 'rest_framework.permissions.IsAuthenticated'
            ),
        },
        CHANNEL_LAYERS={
            "default": {
                "BACKEND": "channels.layers.InMemoryChannelLayer",
            },
        },

        # Static files (CSS, JavaScript, Images)
        # https://docs.djangoproject.com/en/3.0/howto/static-files/


        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                'django.request': {
                    'handlers': ['console'],
                    'level': 'DEBUG',  # change debug level as appropiate
                    'propagate': False,
                },
            },
        }

    )