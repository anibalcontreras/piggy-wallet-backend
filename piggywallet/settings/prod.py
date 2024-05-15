from .base import *
import os
from dotenv import load_dotenv

# DEBUG = False
# ALLOWED_HOSTS = ['mydomain.com']

load_dotenv()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# STATIC_ROOT = '/var/www/mydomain.com/static/'
