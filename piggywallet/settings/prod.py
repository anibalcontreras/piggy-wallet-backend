from .base import *

DEBUG = False
ALLOWED_HOSTS = ['mydomain.com']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "securepassword",
        "HOST": "prod-db-host",
        "PORT": "5432",
    }
}

STATIC_ROOT = '/var/www/mydomain.com/static/'
