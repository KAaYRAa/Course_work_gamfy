import os
from pathlib import Path
from decouple import config
import sys
from django.test.runner import DiscoverRunner

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

LOGIN_URL = 'users:login'          
LOGIN_REDIRECT_URL = 'games:home'  
LOGOUT_REDIRECT_URL = 'users:login'


INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    'channels',
    'rest_framework',
    'django_cleanup.apps.CleanupConfig',
    

    'users',
    'games',  
    'alias',
    'pig',
    'mafia',
    'who_am_i',
    'puzzle',
    'five_seconds',
    'danetki',
    'never_have_i_ever',
    'dilemma',
    'crocodile',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"


ASGI_APPLICATION = "core.asgi.application"
WSGI_APPLICATION = "core.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'], 
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media", 
            ],
        },
    },
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Gamfy',
        'USER': 'postgres', 
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',       
    }
}

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



LANGUAGE_CODE = "uk-ua" 
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


if 'test' in sys.argv:
    class FastTestRunner(DiscoverRunner):
        def setup_databases(self, **kwargs):
            return None
        
        def teardown_databases(self, old_config, **kwargs):
            pass

    TEST_RUNNER = 'core.settings.FastTestRunner'